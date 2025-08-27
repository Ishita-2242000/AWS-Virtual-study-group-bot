import boto3
from datetime import datetime
import uuid

try:
    dynamodb = boto3.resource('dynamodb', region_name = 'us-east-1')

    table = dynamodb.Table('StudySession')

    session_id = f"{uuid.uuid4()}_{datetime.utcnow().isoformat()}"

    item = {
        'session_id' : session_id,
        'user_name' : 'Ishita Chatterjee',
        'user_email' : 'ishita.chatterjee@gmail.com',
        'session_time': '2025-08-04T15:00:00Z',
        'reminder_set': False
    }

    table.put_item(Item = item)

    print('user session added successfully')

except Exception as e:
    print(f"error is {e}")

    