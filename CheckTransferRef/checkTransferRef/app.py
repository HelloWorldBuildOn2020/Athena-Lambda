import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event['body'])
    transfer_ref = body['transferRef']
    message = ''
    if len(transfer_ref) == 18 and transfer_ref.isdigit():
        # save to database and send to Bank api
        # send bank api
        message = 'Sent transferRef to bank api.'
    else:
        message = 'Transfer Ref is invalid.'
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": message,
            # "location": ip.text.replace("\n", "")
        }),
    }
