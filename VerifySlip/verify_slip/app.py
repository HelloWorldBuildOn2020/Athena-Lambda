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
try:
    cursor = conn.cursor()

    select_stmt = "SELECT * FROM users WHERE user_id = %(user_id)s"
    cursor.execute(select_stmt, { 'user_id' : 1 }) 
    user = cursor.fetchall()

    select_company_stmt = "SELECT * FROM company WHERE company_id = %(comany_id)s"
    cursor.execute(select_company_stmt, { 'comany_id' : user[0][0] }) 
    company = cursor.fetchall()
    # cursor.execute("UPDATE table SET attribute='new'")
    # conn.commit()
except(Exception, psycopg2.Error) as error:
    print("Error connecting to PostgreSQL database", error)
    conn = None

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
    filename = user_id + "_" + comany_name.replace(" ", "") + str(datetime.datetime.now().strftime("_%d_%B_%f")) + '.jpg'
 
    s3 = boto3.client('s3')
    get_file_content = event['content']
    decode_content = base64.b64decode(get_file_content)
    s3_upload = s3.put_object(Bucket="slip-test", Key=filename, Body=decode_content, ACL='public-read', ContentType='image/jpeg')

    read_qrcode_url = os.environ['READ_QR_CODE_API'] + '?imageName=' + filename
    response_read_qr_code = requests.request("GET", read_qrcode_url)
    transfer_ref = json.loads(response_read_qr_code.content.decode('utf-8'))['transfer_ref']
 
    response_lambda = client_lambda.invoke(
        FunctionName='CheckTransferRef-CheckTransferRefFunction-1AMZF0WTL9C71',
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
            filename
        )
        try:
            cursor.execute(insert_stmt, value_insert)
            conn.commit()
        except(Exception, psycopg2.Error) as error:
            print("Error connecting to PostgreSQL database", error)
            conn = None
        finally:
            if(conn != None):
                cursor.close()
                conn.close()
                print("PostgreSQL connection is now closed")
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
   
