#Example of triggering a step function using lambda

import os
import json
#from uuid import uuid4

import boto3

client = boto3.client('stepfunctions')

state_machine_arn = os.environ['state_machine']


def handler(event, context):
    print(event)

    #condense the s3 object details
    s3_details = {
        'key': event['Records'][0]['s3']['object']['key'],
        'bucket': event['Records'][0]['s3']['bucket']['name']
        'animate': []
    }

    #list radar ids to animate
    s3_details['animate'] = 'IDR762'

    print(s3_details)

    #state machine needs to be started with a unique 'name'
    #the key is good to use because it is unique and will
    #be useful for debugging - need to replace '/' with '_'
    name = s3_details['key'].replace('/','_')

    #for _testing_ use a uuid
    #name = str(uuid4())[0:6]

    response = client.start_execution(
        stateMachineArn=state_machine_arn,
        name=name,
        input=json.dumps(s3_details)
    )

    return {}

#local testing
#from test import event as e
#ev = json.loads(e)

#handler(ev,{})
