import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudySession')

def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']

    # Get slot values safely
    username = get_slot_value(slots, 'username')
    user_email = get_slot_value(slots, 'user_email')
    session_topic = get_slot_value(slots, 'session_topic')
    session_date = get_slot_value(slots, 'session_date')
    session_time = get_slot_value(slots, 'session_time')

    # Capitalize username if present
    if username:
        username = username.capitalize()
        set_slot_value(slots, 'username', username)

    # Let Lex handle slot prompting
    if not all([username, user_email, session_topic, session_date, session_time]):
        return delegate_to_lex(intent_name, slots)

    # Save to DynamoDB
    session_id = f"{uuid.uuid4()}_{datetime.utcnow().isoformat()}"
    table.put_item(
        Item={
            'session_id': session_id,
            'username': username,
            'user_email': user_email,
            'session_topic': session_topic,
            'session_date': session_date,
            'session_time': session_time,
            'timestamp': datetime.utcnow().isoformat()
        }
    )

    # Final fulfillment message
    fulfillment_message = (
        f"Thanks {username}, I've successfully enrolled you to "
        f"{session_topic} class on {session_date} at {session_time} successfully! "
        f"You'll be receiving an email on {user_email} 15 mins before the entered time."
    )

    return close_intent(intent_name, fulfillment_message)

# ---------------- Utility Functions ---------------- #

def get_slot_value(slots, slot_name):
    """Safely extract slot value."""
    slot = slots.get(slot_name)
    if slot and slot.get('value'):
        return slot['value'].get('interpretedValue')
    return None

def set_slot_value(slots, slot_name, value):
    """Set updated value for a slot."""
    if slot_name in slots and slots[slot_name]:
        slots[slot_name]['value']['interpretedValue'] = value

def delegate_to_lex(intent_name, slots):
    """Delegate slot filling back to Lex."""
    return {
        "sessionState": {
            "dialogAction": {"type": "Delegate"},
            "intent": {
                "name": intent_name,
                "slots": slots,
                "state": "InProgress"
            }
        }
    }

def close_intent(intent_name, message):
    """Close the intent and return a message."""
    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {
                "name": intent_name,
                "state": "Fulfilled"
            }
        },
        "messages": [
            {"contentType": "PlainText", "content": message}
        ]
    }