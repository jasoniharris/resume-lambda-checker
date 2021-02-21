import boto3
import os
import uuid
import datetime
import json
import urllib3

VERBOSE = 1

def send_sns(requestID, date, error):
    """ Sending notification about new post to SNS """
    print("Sending SNS notification")
    arn = os.environ['SNSTOPIC']
    message = "Website Down"
    client = boto3.client('sns', region_name='eu-west-2')
    response = client.publish(
        TargetArn=arn,
        Message=(error + "\n RequestID: " + requestID + "\n Date: " + date),
    )

def check_domain(domain):
    requestID = str(uuid.uuid4())
    date = str(datetime.datetime.now())
    try:
        http = urllib3.PoolManager()
        r = http.request('GET', domain)
        status_code=r.status
        print(f"Checking {domain} : {status_code}")
        """ Validate website is active """
        if status_code != 200:
            error = f'Website {domain} is down: Response Code: {status_code}'
            print(error)
            print(r.data)
            try:
                """ Sending notification about new post to SNS """
                send_sns(requestID, date, error)
            except Exception as e: 
                error = f'Failed to send SNS: {e}'
                print(f'{error} | {requestID} | {date}')
                send_sns(requestID, date, error)
                exit(1)
    except Exception as e: 
        error = f'HTTPS Request failed: {e}'
        send_sns(requestID, date, error)
        exit(1)

def handler(event, context):
    check_domain("https://jasoniharris.com")

