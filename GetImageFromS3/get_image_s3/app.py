import json
import boto3

client = boto3.client('s3')
def lambda_handler(event, context):
    # It mock up key. We will change it when Verify slip function is finish.
    # https://slip-test.s3-ap-southeast-2.amazonaws.com/06_August_025421.jpg
    bucket = 'slip-test'
    key = '06_August_025421.jpg'
    bucket_location = boto3.client('s3').get_bucket_location(Bucket=bucket)
    obj_url = 'https://' + bucket + '.s3-' + bucket_location['LocationConstraint'] + '.amazonaws.com/' + key
    return {
        "statusCode": 200,
        "body": json.dumps({
            "obj_url": obj_url,
        }),
    }
