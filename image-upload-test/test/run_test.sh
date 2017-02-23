#!/bin/bash

URL=$1

IMAGE_SMALL=88k_file.jpg
IMAGE_MEDIUM=1.5MB_file.jpg
IMAGE_LARGE=2.9M_file.jpg

#small
BASE64_SMALL_RESULT=./base64_small_results.txt
PRESIGN_SMALL_RESULT=./presign_small_results.txt
#medium
BASE64_MEDIUM_RESULT=./base64_medium_results.txt
PRESIGN_MEDIUM_RESULT=./presign_medium_results.txt
#large
BASE64_LARGE_RESULT=./base64_large_results.txt
PRESIGN_LARGE_RESULT=./presign_large_results.txt

#clear results files
> $BASE64_SMALL_RESULT
> $PRESIGN_SMALL_RESULT
> $BASE64_MEDIUM_RESULT
> $PRESIGN_MEDIUM_RESULT
> $BASE64_LARGE_RESULT
> $PRESIGN_LARGE_RESULT

while [ 1 ]
do
  #small file

  { time -p  ./base64_request.sh $URL $IMAGE_SMALL ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $BASE64_SMALL_RESULT
  { time -p  ./presign_request.sh $URL $IMAGE_SMALL ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $PRESIGN_SMALL_RESULT

  #medium file

  { time -p  ./base64_request.sh $URL $IMAGE_MEDIUM ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $BASE64_MEDIUM_RESULT
  { time -p  ./presign_request.sh $URL $IMAGE_SMALL ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $PRESIGN_MEDIUM_RESULT

  #large file

  { time -p  ./base64_request.sh $URL $IMAGE_LARGE ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $BASE64_LARGE_RESULT
  { time -p  ./presign_request.sh $URL $IMAGE_LARGE ; } 2>&1 >/dev/null \
    | head -n 1 | awk '{print $2}' >> $PRESIGN_LARGE_RESULT

done
