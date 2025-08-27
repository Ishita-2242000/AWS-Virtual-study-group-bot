import boto3

lexv2 = boto3.client('lexv2-models', region_name='us-east-1')



response = lexv2.create_bot_locale(
    botId = 'Z6C1AOE4F8',  # Replace with actual bot ID
    botVersion='DRAFT',
    localeId='en_US',
    description='English locale for study group bot',
    nluIntentConfidenceThreshold=0.4  # how confident Lex should be before triggering an intent
)

locale_id =  response['localeId']

print(locale_id)

# lexv2.delete_bot_locale(
#     botId='ENAARD8CJ7',
#     botVersion='DRAFT',
#     localeId='en_US'
# )