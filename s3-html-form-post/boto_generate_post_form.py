import boto3
from pprint import pprint

client = boto3.client('s3')

post = client.generate_presigned_post('aws-meetup-hobart', 'somefile.txt', None, None, ExpiresIn=600)

pprint(post)
