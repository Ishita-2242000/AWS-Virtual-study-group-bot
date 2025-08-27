import boto3
import json
import time
iam = boto3.client('iam')

role_name = 'MyLambdaExecutionRole'

assume_role_policy = {
    'Version' : '2012-10-17',
    'Statement' : [
        {
            'Effect' : 'Allow',
            'Principal' : {
                'Service' : 'lambda.amazonaws.com'
            },
            'Action' : 'sts:AssumeRole'
        }
    ]
}
try:
    response = iam.create_role(
        RoleName = role_name,
        AssumeRolePolicyDocument = json.dumps(assume_role_policy),
        Description = 'Role for Lambda to write to CloudWatch'
)
    print(f"role {role_name} is created successfully")
except iam.exceptions.EntityAlreadyExistsException:
    print(f"[!] Role '{role_name}' already exists. Skipping creation.")
policy_arn = 'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'

iam.attach_role_policy(
    RoleName = role_name,
    PolicyArn = policy_arn
)

print(f"[✓] Attached AWSLambdaBasicExecutionRole policy.")

# Wait for role to propagate before using it
print("[⏳] Waiting for IAM role to propagate...")
time.sleep(10)

# Get and print role ARN
role = iam.get_role(RoleName=role_name)
role_arn = role['Role']['Arn']
print(f"[✓] Role ARN: {role_arn}")