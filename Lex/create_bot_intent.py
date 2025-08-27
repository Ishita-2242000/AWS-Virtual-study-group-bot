import boto3


lexv2 = boto3.client('lexv2-models', region_name='us-east-1')

response = lexv2.create_intent(
    botId= 'BDUBFLMIGZ',  # Replace with your actual bot ID
    botVersion='DRAFT',
    localeId= 'en_US',
    intentName='RegisterStudySession',
    sampleUtterances=[
        {'utterance': 'I want to join a study session'},
        {'utterance': 'Register me for a session'},
        {'utterance': 'Sign me up for study group'},
        {'utterance': 'Book my study session'}
    ],
    description='Handles study session registrations.'
)

intent_id =  response['intentId']

print(intent_id)