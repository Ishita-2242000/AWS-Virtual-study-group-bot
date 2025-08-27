import boto3

client = boto3.client('lexv2-models')

def create_slot(slot_name, slot_type, prompt, bot_id, intent_id):
    response = client.create_slot(
        botId=bot_id,
        botVersion='DRAFT',
        localeId='en_US',
        intentId=intent_id,
        slotName=slot_name,
        slotTypeId=slot_type,
        valueElicitationSetting={
            'slotConstraint': 'Required',
            'promptSpecification': {
                'messageGroups': [{
                    'message': {
                        'plainTextMessage': {
                            'value': prompt
                        }
                    }
                }],
                'maxRetries': 2
            }
        }
    )
    print(f"{slot_name} slot created:", response['slotId'])

# Use prebuilt slot types or custom ones         
# create_slot('username','AMAZON.AlphaNumeric', "What is your name?",'BDUBFLMIGZ','T9OLBVQLYB')
# create_slot('user_email','AMAZON.EmailAddress', "Kindly provide the email id",'BDUBFLMIGZ','T9OLBVQLYB')
create_slot('session_topic', 'AMAZON.AlphaNumeric', "What topic is the study session about?", "BDUBFLMIGZ", "T9OLBVQLYB")
create_slot('session_date', 'AMAZON.Date', "On what date is the session?", "BDUBFLMIGZ", "T9OLBVQLYB")
create_slot('session_time', 'AMAZON.Time', "At what time is the session?", "BDUBFLMIGZ", "T9OLBVQLYB")
