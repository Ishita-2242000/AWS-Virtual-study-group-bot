import boto3

dynamodb = boto3.client('dynamodb', region_name = 'us-east-1')

table_name = 'StudySession'

try:
    response = dynamodb.create_table(
        TableName = table_name,
        AttributeDefinitions = [
            {
                'AttributeName' : 'session_id',
                'AttributeType' : 'S'
            }
        ],
        KeySchema = [
            {
                'AttributeName' : 'session_id',
                'KeyType' : 'HASH'
            }
        ],
        ProvisionedThroughput = 
            {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
)

    print("table status : ", response['TableDescription']['TableStatus'])

except dynamodb.exceptions.ResourceInUseException:
    print(f"Table {table_name} already exists.")