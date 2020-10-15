import boto3
import json
import os
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

select_email_stmt = "SELECT * FROM email_subscription WHERE company_id = %(company_id)s"
cursor.execute(select_email_stmt, { 'company_id' : 1 }) 
email = cursor.fetchall()

sns = boto3.client('sns')
def lambda_handler(event, context):
    fail_amount = event['amount']
    fail_date = event['date']
    fail_time = event['time']
    fail_image = event['image_from_s3']
    
    email_body = 'Hello, \nResult of fail to verify\n' + \
        'Amount: ' + fail_amount + '\n' + \
        'Date: ' + fail_date + '\n' + \
        'Time: ' + fail_time + '\n' + \
        'Image: ' + fail_image + '\n' + \
        'You can check on https://athena.khotor.live/' + '\n' + \
        'Best Regards, \nAthena'
    
    for each_email in email:
        subscription = sns.subscribe(
            TopicArn=os.environ['TopicArn'],
            Protocol='email',
            Endpoint=each_email[0],
            ReturnSubscriptionArn=True
        )

    response = sns.publish(
        TopicArn=os.environ['TopicArn'],    
        Message=email_body,
        Subject='Athena'
    )

    return {
        "statusCode": 200,
        "body": {
            "message": "Send Email Success!"
        },
    }