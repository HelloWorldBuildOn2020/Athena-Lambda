import json
import boto3
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
tables = cursor.execute("SELECT * FROM users;")
print(cursor.fetchall())
# cursor.execute("UPDATE table SET attribute='new'")
# conn.commit()
cursor.close()


client = boto3.client('redshift')
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
