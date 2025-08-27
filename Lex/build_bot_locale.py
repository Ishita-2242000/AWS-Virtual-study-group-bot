import boto3
import time
lexv2 = boto3.client('lexv2-models', region_name='us-east-1')

# After create_bot_locale
response = lexv2.build_bot_locale(
    botId='BDUBFLMIGZ',
    botVersion='DRAFT',
    localeId='en_US'
)

while True:
    response = lexv2.describe_bot_locale(
        botId='BDUBFLMIGZ',
        botVersion='DRAFT',
        localeId='en_US'
    )
    status = response['botLocaleStatus']
    print("Current status:", status)
    if status == 'Built':
        break
    elif status in ['Failed', 'Deleting']:
        raise Exception("Bot Locale build failed.")
    time.sleep(5)