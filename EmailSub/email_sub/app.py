import json
import os
import psycopg2


database = os.environ['DATABASE']
port = os.environ['PORT']
user = os.environ['USER_DB']
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

def lambda_handler(event, context):
    email_sub = []
    for each_email in email:
        email_sub.append(
        {
            "email": each_email[0]
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(email_sub),
    }
