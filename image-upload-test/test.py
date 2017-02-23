import base64
import json
import boto3

client = boto3.client('s3')

with open('test_payload.json') as fp:
    base64_image = base64.b64decode(json.loads(json.loads(fp.read())['body'])['base64'])

response = client.put_object(
    Bucket="s3uploadtest.gsat.technology",
    Key="tiger.jpg",
    Body=base64_image
)

print response
