import os
import boto3
from datetime import datetime, timedelta, timezone

# ——————————— CONFIG ———————————
TABLE_NAME   = "StudySession"                 # DynamoDB table
SENDER_EMAIL = "chatterjeeishita231@gmail.com"  # Verified sender in SES
SES_REGION   = "us-east-1"                    # Region where SES identities live

# Toggle TEST mode with an environment variable:
# • TEST_MODE = "1"  ➜  hard-coded test time (see below)
# • anything else   ➜  real clock
TEST_MODE = os.getenv("TEST_MODE", "0") == "1"
TEST_TIME_IST = "2025-08-16 22:20"            # <-- adjust when testing

# ——————————— AWS CLIENTS ———————————
dynamodb = boto3.resource("dynamodb")
ses       = boto3.client("ses", region_name=SES_REGION)

table = dynamodb.Table(TABLE_NAME)
IST   = timezone(timedelta(hours=5, minutes=30))  # Asia/Kolkata offset

# ——————————— LAMBDA HANDLER ———————————
def lambda_handler(event, context):
    # 1. Current time (UTC)
    if TEST_MODE:
        now_ist = datetime.strptime(TEST_TIME_IST, "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        now_utc = now_ist.astimezone(timezone.utc)
    else:
        now_utc = datetime.now(timezone.utc)

    reminders = []

    # 2. Scan table for upcoming sessions that have NOT been reminded
    response = table.scan(FilterExpression="attribute_not_exists(reminder_sent) OR reminder_sent = :f",
                          ExpressionAttributeValues={":f": False})
    for item in response["Items"]:
        # Required attributes
        session_date = item.get("session_date")   # e.g. "2025-08-16"
        session_time = item.get("session_time")   # e.g. "22:35"
        user_email   = item.get("user_email")
        username     = (item.get("username") or "").capitalize()

        if not (session_date and session_time and user_email):
            continue  # skip incomplete records

        # 3. Build session datetime in IST, convert to UTC
        session_dt_ist = datetime.strptime(f"{session_date} {session_time}", "%Y-%m-%d %H:%M").replace(tzinfo=IST)
        session_dt_utc = session_dt_ist.astimezone(timezone.utc)

        # 4. Should we send a reminder?
        reminder_time_utc = session_dt_utc - timedelta(minutes=15)
        if reminder_time_utc <= now_utc <= session_dt_utc:
            send_email(user_email, session_dt_ist, username)
            mark_reminded(item["session_id"])  # assumes partition key = session_id
            reminders.append(user_email)

    return {
        "reminders_sent": reminders,
        "now_utc": now_utc.isoformat()
    }

# ——————————— HELPERS ———————————
def send_email(to_email, session_dt_ist, username):
    subject = "Reminder: Your Study Session Starts Soon"
    body = (
        f"Hi {username},\n\n"
        f"This is a friendly reminder that your study session starts at "
        f"{session_dt_ist.strftime('%H:%M IST on %d-%b-%Y')}.\n\n"
        "See you there!\n"
        "— Study Bot"
    )

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [to_email]},
        Message={
            "Subject": {"Data": subject},
            "Body":    {"Text": {"Data": body}}
        }
    )

def mark_reminded(session_id):
    table.update_item(
        Key={"session_id": session_id},
        UpdateExpression="SET reminder_sent = :t",
        ExpressionAttributeValues={":t": True}
    )