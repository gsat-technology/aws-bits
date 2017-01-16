import os
import boto3

client = boto3.client('s3')
bucket = os.environ['s3_bucket']

def handler(event, context):
    """
    generatePresignPOST
    """

    file = event['filename']

    url = client.generate_presigned_post(
                                        Bucket=bucket, Key='/uploads/' + file,
                                        Fields=None,
                                        Conditions=None,
                                        ExpiresIn=300)
    print url
    return url
