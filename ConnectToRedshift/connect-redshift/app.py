import json
import boto3
import pymysql
import os
import sys
import logging

db_host  = os.getenv('db_host')
name = os.getenv('db_username')
password = os.getenv('db_password')
db_name = os.getenv('db_name')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(db_host, user=name, passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

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
