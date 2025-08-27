from datetime import datetime
import boto3

lexv2 = boto3.client('lexv2-models', region_name='us-east-1')

response = lexv2.create_bot(
    botName='StudyGroupBot',
    description='Helps users register for study sessions.',
    roleArn='arn:aws:iam::489975610637:role/aws-service-role/lexv2.amazonaws.com/AWSServiceRoleForLexV2Bots_LexBotServiceRole',
    dataPrivacy={'childDirected': False},
    idleSessionTTLInSeconds=300,
    botType='Bot'
)

bot_id =  response['botId']

print(bot_id)
