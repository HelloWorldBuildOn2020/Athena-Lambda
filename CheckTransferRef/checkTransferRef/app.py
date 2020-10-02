import json
import boto3
import requests

def lambda_handler(event, context):
    transfer_ref = event['transferRef']
    message = ''
    if len(transfer_ref) == 18 and transfer_ref.isdigit():
        # save to database and send to Bank api
        # send bank api
        url = "https://openapi-sandbox.kasikornbank.com/v1/verslip/kbank/verify"
        payload = "{\r\n    \"rqUID\": \"783_20191108_v4UIS1K2Mobile\",\r\n    "
        payload += "\"rqDt\": \"2019-11-05T17:00:00.966+07:00\",\r\n    "
        payload += "\"data\": {\r\n        \"sendingBank\": \"004\",\r\n   "
        payload += "     \"transRef\": \"" + transfer_ref + "\"\r\n    }\r\n}"

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer a2FzaWtvcm5iYW5rdG9rZW4='
        }

        bank_response = requests.request("POST", url, headers=headers, data=payload)

        json_bank_response = json.loads(bank_response.content.decode('utf8').replace(" ", ""))
        
        return json_bank_response
    else:
        return 'Transfer Ref invalid.'