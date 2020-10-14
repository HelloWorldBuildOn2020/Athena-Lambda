import json
import requests
import os
import sys

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

def lambda_handler(event, context):
    user_id = 1
    cursor = conn.cursor()

    select_stmt = "SELECT * FROM users WHERE user_id = %(user_id)s"
    cursor.execute(select_stmt, { 'user_id' : user_id }) 
    user = cursor.fetchall()

    select_company_stmt = "SELECT * FROM company WHERE company_id = %(comany_id)s"
    cursor.execute(select_company_stmt, { 'comany_id' : user_id }) 
    company = cursor.fetchall()

    select_slip_stmt = "SELECT * FROM slip WHERE user_id = %(user_id)s"
    cursor.execute(select_slip_stmt, { 'user_id' : user_id }) 
    slips = cursor.fetchall()
    list_slips = []
    for item in range(len(slips)):
        list_slips.append(
            {
                "transfer_ref": str(slips[item][0]),
                "user_id": str(slips[item][1]),
                "bank_sending": str(slips[item][2]),
                "amount": float(slips[item][3]),
                "date": str(slips[item][4]),
                "time": str(slips[item][5]),
                "image_name": str(slips[item][6]),
                "status": str(slips[item][7])
            }
        )

    return {
        "statusCode": 200,
        "body": json.dumps(list_slips)
    }
