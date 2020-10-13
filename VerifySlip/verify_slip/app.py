import json
import boto3
import requests
import base64
import datetime
import os
import sys
import logging
import psycopg2

database = os.environ['DATABASE']
port = os.environ['PORT']
user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']

conn = psycopg2.connect(
    database=database,
    port=port,
    user=user,
    password=password,
    host=host
)

cursor = conn.cursor()

select_stmt = "SELECT * FROM users WHERE user_id = %(user_id)s"
cursor.execute(select_stmt, { 'user_id' : 1 }) 
user = cursor.fetchall()

select_company_stmt = "SELECT * FROM company WHERE company_id = %(comany_id)s"
cursor.execute(select_company_stmt, { 'comany_id' : user[0][0] }) 
company = cursor.fetchall()
# cursor.execute("UPDATE table SET attribute='new'")
# conn.commit()

client = boto3.client('rekognition')
client_lambda = boto3.client('lambda')

def lambda_handler(event, context):
    param_querystrings = event['params']['querystring']
    amount = param_querystrings['amount']
    date = param_querystrings['date']
    time = param_querystrings['time']
    user_id = param_querystrings['user_id']

    # image name = userid + company name + date + .jpg
    user_id = str(user[0][1])
    comany_name = company[0][1]
    filename = user_id + "_" + comany_name + str(datetime.datetime.now().strftime("_%d_%B_%f")) + '.jpg'
 
    s3 = boto3.client('s3')
    get_file_content = event['content']
    decode_content = base64.b64decode(get_file_content)
    s3_upload = s3.put_object(Bucket="slip-test", Key=filename, Body=decode_content, ACL='public-read', ContentType='image/jpeg')
    
    response = client.detect_text(
        Image={
            'S3Object': {
                'Bucket': 'slip-test',
                'Name': filename
            }
        }
    )

    transfer_ref = response['TextDetections'][13]['DetectedText']

    response_lambda = client_lambda.invoke(
        FunctionName='CheckTransferRef-HelloWorldFunction-1JXCD98X6QC7K',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps({ 'transferRef': transfer_ref }),
    )

    payload = json.load(response_lambda['Payload'])

    bank_response = payload['data']
    bank_date = bank_response['transDate']
    bank_time = bank_response['transTime'][0:5]
    bank_paidLocalCurrency = bank_response['paidLocalCurrency']
    bank_message_status = payload['statusMessage']

    conditions = (bank_date == date) & (bank_time == time) & (bank_paidLocalCurrency == amount) & (bank_message_status == "SUCCESS") 
    if conditions:
        insert_stmt = """ INSERT INTO slip VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        value_insert = (
            transfer_ref,
            user_id,
            bank_response['sendingBank'],
            bank_paidLocalCurrency,
            bank_date,
            bank_time,
            datetime.datetime.now()
        )
        cursor.execute(insert_stmt, value_insert)
        conn.commit()
        cursor.close()
        return {
            "statusCode": 200,
            "image_file": json.dumps(filename)
        } 
    else:
        response = {
            "statusCode": 400,
            "body": "Bad Request."
        }
        trigger_sns(date, time, filename)
        raise Exception("Status code 400: Bad request.")

def trigger_sns(date, time, filename):
    invoke_trigger_sns = client.invoke(
        FunctionName='TriggerSNS-TriggerSNSFunction-16NJMO6YBYMVX',
        InvocationType='RequestResponse',
        LogType='Tail',
        Payload=json.dumps({ 
            'date': date,
            'time' : time,
            'image_from_s3' : filename
        })
    )
   
