import boto3

boto3.setup_default_session(profile_name='DataTeam')
client = boto3.client('stepfunctions', endpoint_url='http://localhost:8083')
client.start_execution(
    stateMachineArn='arn:aws:states:us-east-1:123456789012:stateMachine:TestStateMachine#POCTest',
    name='HelloWorld-StateMachine-1',
    input='{}'
)
