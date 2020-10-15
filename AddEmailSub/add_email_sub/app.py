import json
import os
import psycopg2


database = os.environ['DATABASE']
port = os.environ['PORT']
user = os.environ['USER']
password = os.environ['PASSWORD']
host = os.environ['HOST']


def lambda_handler(event, context):
    email_event = event['email']
    
    conn = psycopg2.connect(
        database=database,
        port=port,
        user=user,
        password=password,
        host=host
    )

    cursor = conn.cursor()

    select_email_stmt = "SELECT * FROM email_subscription WHERE email = %(email)s"
    cursor.execute(select_email_stmt, { 'email' : email_event }) 
    email = cursor.fetchall()

    insert_email_stmt = "INSERT INTO email_subscription (email, company_id) VALUES (%s, %s)"
    value_insert = ()

    if len(email) == 0:
        value_insert = (
            email_event,
            1
        )
        cursor.execute(insert_email_stmt, value_insert)
        conn.commit()
        return {
            "statusCode": 200,
            "message": "Add email success!"
        }
    else:
        raise Exception("Status code 400: Bad request. This Email already exited")
