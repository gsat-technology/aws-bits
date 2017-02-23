#!/bin/bash

URL=$1
S3_BUCKET=$2

FILE_ARRAY+=('./testfiles/256KB.file')
FILE_ARRAY+=('./testfiles/512KB.file')
FILE_ARRAY+=('./testfiles/1MB.file')



for i in {1..31}
do    
    for f in ${FILE_ARRAY[@]}
    do
	#base64 upload via API Gateway
        base64=$(base64 $f)
	payload="{\"filename\": \"apigupload.file\", \"base64\": \"$base64\"}"
       
        { time -p echo $payload | curl -s -X POST -H "Content-Type: application/json" -d @- $URL/base64upload 2>&1 >> /dev/null ; } 2> /tmp/apig.out

	REAL_TIME=$(cat /tmp/apig.out | head -n 1 | awk '{print $2}')
	printf "$REAL_TIME\t"

	#2-stage upload using Presigned URL
	{ time -p ./presign_request.sh $URL $f 2>&1 >/dev/null ; } 2> /tmp/apig.out
	REAL_TIME=$(cat /tmp/apig.out | head -n 1 | awk '{print $2}')
	printf "$REAL_TIME\t"
	
	#AWS CLI upload
	{ time -p aws s3 cp $f s3://$S3_BUCKET > /dev/null ; } 2> /tmp/apig.out
	REAL_TIME=$(cat /tmp/apig.out | head -n 1 | awk '{print $2}')
        printf "$REAL_TIME\t"
    done

    echo ""
done


