import boto3
import json
import os

sns = boto3.client('sns')
def lambda_handler(event, context):
    fail_date = event['date']
    fail_time = event['time']
    fail_image = event['image_from_s3']
    
    email_body = 'Hello, \nResult of fail to verify\n' + \
        'Date: ' + fail_date + "\n" +\
        'Time: ' + fail_time + "\n" +\
        'Image: ' + fail_image + "\n" +\
        'Best Regards, \nAthena'
    
    response = sns.publish(
        TopicArn=os.environ['TopicArn'],    
        Message=email_body,
        Subject='Athena'
    )
    return {
        "statusCode": 200,
        "body": {
            "message": "Send Email Success!",
        },
    }