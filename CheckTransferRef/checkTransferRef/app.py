import json

def lambda_handler(event, context):
    print('Hello')
    hi = "123"
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
