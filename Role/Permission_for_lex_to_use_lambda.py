import boto3

lambda_client = boto3.client('lambda')

lambda_function_name = 'LexDialogHook'  # Replace with your Lambda function name
lex_bot_arn = 'arn:aws:lex:us-east-1:078805860452:bot-alias/StudyGroupBot/DRAFT'  # Replace this ARN

response = lambda_client.add_permission(
    FunctionName=lambda_function_name,
    StatementId='LexInvokePermissionId',
    Action='lambda:InvokeFunction',
    Principal='lex.amazonaws.com',
    SourceArn=lex_bot_arn
)

print("Permission added:", response)
