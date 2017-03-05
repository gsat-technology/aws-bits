
#boto3 example of using a worker process

import json
import os
from uuid import uuid4
import sys
from time import sleep

import wand
from wand.image import Image
import boto3
import arrow

region = 'ap-northeast-1'

client = boto3.client('stepfunctions', region_name=region)
activity_arn = 'arn:aws:states:ap-northeast-1:xxxxxxxxxxxx:activity:<activity_name>'

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')


def print_t(msg):
    h = arrow.utcnow().to('Australia/Hobart').format('[YYYY-MM-DD HH:mm:ss]')
    print('{}: {}'.format(h, msg))


#returns a list of objects from the 'prefix' section of the 'bucket'
#with 'hours' from earliest to most recent ending at 'latest_object'
def list_images_to_animate(bucket, prefix, hours, latest_key):

    #number of recent objects to skim
    num_objects = hours * 10 #there's 6 images per hour

    #get _everything_ from this folder
    res = s3_resource.Bucket(bucket).objects.filter(Prefix=prefix)

    print('starting for loop over objects')
    objects = [obj.key for obj in res]
    print('finished for loop over objects')

    #slice off objects that are later in the list than 'latest_key'
    latest_index = objects.index(latest_key)
    objects = objects[:latest_index+1]

    #now take the last 'hours' worth of objects prior
    objects = objects[-10*hours:]
    return objects


#downloads images to /tmp and returns list of file locations
def download_flattened_images(bucket, flat_images_lst):

    local_files_lst = []

    for obj_key in flat_images_lst:
        local_file = '/tmp/{}'.format(str(uuid4()))
        s3_client.download_file(bucket, obj_key, local_file)
        local_files_lst.append(local_file)

    return local_files_lst


def delete_temporary_files(local_files_lst):

    for fn in local_files_lst:
        os.remove(fn)

while True:

    print_t('new task')

    response = client.get_activity_task(
      activityArn=activity_arn,
      workerName='ec2 worker'
    )

    #with SFN
    input = json.loads(response['input'])
    bucket = input['bucket']
    key = input['key']
    hours = input['hours']

    print_t('bucket: {} key: {} hours: {}'.format(bucket, key, str(hours)))

    #the prefix key for where to find the flattened files
    key_split = key.split('/')
    file_timestamp = key_split.pop().replace('jpeg','')
    flattened_prefix = '/'.join(key_split)

    flat_images_lst = list_images_to_animate(bucket, flattened_prefix, max(hours), key)
    print_t('num images to animate: {}'.format(str(len(flat_images_lst))))

    local_files_lst = download_flattened_images(bucket, flat_images_lst)

    for h in hours:

        print_t('processing hour: {}'.format(h))

        #get a slice of the files depending on the hours
        sub_local_files_lst = local_files_lst[-10*h:]
        print_t('num images for {} hour(s): {}'.format(str(h), str(len(sub_local_files_lst))))

        #local file to temporarily save animated gif to disk
        local_file = '/tmp/{}.gif'.format(str(uuid4()))

        #s3 target to put animate gif
        key_split = key.split('/')
        remote_key = 'animated/{}/{}/{}/{}'.format(key_split[1], key_split[2], str(h), key_split[3])
        remote_key = remote_key.replace('jpeg', 'gif')

        with Image() as w:
            for fn in sub_local_files_lst:
                i = Image(filename=fn)
                w.sequence.append(i)

            wand.type = 'optimize'
            w.save(filename=local_file)

        s3_client.upload_file(local_file, bucket, remote_key, ExtraArgs={"ContentType": "image/gif"})
        print_t('gif uploaded to s3: {}'.format(remote_key))

    #clean up
    delete_temporary_files(local_files_lst)

    #form the response

    output = {
        'bucket': bucket,
        'animated_gif_key': remote_key,
        'do_tweet': None
    }

    timestamp = arrow.get(file_timestamp, 'YYYYMMDDHHmm')

    #if top of the hour and hour is 0000, 0600, 1200 or 1800
    #if hobart_time.minute == 0 and (hobart_time.hour % 6) == 0:

    #if timestamp.minute == 0 and True:
    if True:
        output['do_tweet'] = True
    else:
        output['do_tweet'] = False

    print_t(json.dumps(output))

    response = client.send_task_success(
      taskToken=response['taskToken'],
      output=json.dumps(output)
    )

    print_t('finished task')

    sleep(1)
