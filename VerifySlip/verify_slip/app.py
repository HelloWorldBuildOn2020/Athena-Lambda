import json
import boto3
import requests

client = boto3.client('rekognition')
client_lambda = boto3.client('lambda')

def lambda_handler(event, context):
    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': 'slip-test',
                'Name': event['s3_slip_name']
            }
        }
    )

    response_lambda = client_lambda.invoke(
        FunctionName='CheckTransferRef-HelloWorldFunction-RLYO4TK5PFME',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps({ 'transferRef': response['TextDetections'][13]['DetectedText'] }),
    )

    payload = json.load(response_lambda['Payload'])
    return {
        "statusCode": 200,
        "body": payload['body']
    }

   
