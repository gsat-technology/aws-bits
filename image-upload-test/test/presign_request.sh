#!/bin/bash

#uploads image in 2-step:
# - json data sent to APIG which responds with presigned url
# - image uploaded using POST to presigned url


APIG=$1
IMAGE_FILE=$2

uuid=$(uuidgen | awk '{print tolower($0)}')
id=${uuid:0:8}

payload="{\"id\": \"$id\"}"

result=$(curl -d "$payload" -H "Accept: application/json" $APIG/image/ 2>/dev/null | jq --raw-output '.presign | .url , .fields.policy , .fields.AWSAccessKeyId , .fields."x-amz-security-token" , .fields.key , .fields.signature')


#organise the details for presign into an array
presign_arr=()
while read -r line
do
   presign_arr+=("$line")
done <<< "$result"


#upload file using presigned-url

# curl -v -X POST  \
#   -F "policy=${presign_arr[1]}" \
#   -F "AWSAccessKeyId=${presign_arr[2]}" \
#   -F "x-amz-security-token=${presign_arr[3]}" \
#   -F "key=${presign_arr[4]}" \
#   -F "signature=${presign_arr[5]}" \
#   -F "file=@$IMAGE_FILE" \
#   ${presign_arr[0]}



http -f POST ${presign_arr[0]} \
  policy=${presign_arr[1]} \
  AWSAccessKeyId=${presign_arr[2]} \
  x-amz-security-token=${presign_arr[3]} \
  key=${presign_arr[4]} \
  signature=${presign_arr[5]} \
  file@$IMAGE_FILE
