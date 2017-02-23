import json
import uuid
import base64
import os
from datetime import datetime

import boto3


client = boto3.client('s3')
bucket = os.environ['s3_bucket']

def handler(event, context):
    print(json.dumps(event))


    if event['httpMethod'] == 'POST':

        body = json.loads(event['body'])
        _id = body['id']

        #get base64 encoded images and PUT in S3
        if 'base64' in body:
            image = base64.b64decode(body['base64'])

            result = client.put_object(
                Bucket=bucket,
                Body=image,
                Key='{}.jpg'.format(body['id']))

            print(json.dumps(result))

            response_body = {"success": "true"}

        if 'binary' in body:
            print('got binary')
            binary = body['binary']

            result = client.put_object(
                Bucket=bucket,
                Body=binary,
                Key='{}.jpg'.format(body['id']))

            print(json.dumps(result))

            response_body = {"success": "true"}
        else:
            presign = client.generate_presigned_post(
                                            Bucket=bucket,
                                            Key=_id + '.jpg',
                                            Fields=None,
                                            Conditions=None,
                                                ExpiresIn=86400)

            response_body = {"presign": presign}

    response = {
        "headers": {},
        "statusCode": 200,
        "body": json.dumps(response_body)
    }

    return response
