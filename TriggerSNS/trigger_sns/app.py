import boto3
import json
import os

def lambda_handler(event, context):
    sns = boto3.client('sns')
    response = sns.publish(
        TopicArn=os.environ['TopicArn'],    
        Message='Check Fail!',
        Subject='Athena'
    )
    return {
        "statusCode": 200,
        "body": {
            "message": "Send Email!",
        },
    }