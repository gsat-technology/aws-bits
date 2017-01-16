#!/bin/bash

#run using: ./lambda_deploy.sh <s3 bucket>
TMP_DIR=/tmp/deployment_packages
S3_BUCKET=$1
LAMBDAS=$(ls lambda_code)
APP_NAME=${PWD##*/}

mkdir -p $TMP_DIR

for lambda in $LAMBDAS
do
    echo "processing $lambda"
    cd ./lambda_code/$lambda
    zip -r $TMP_DIR/$lambda.zip *
    cd ../../

    aws s3 cp $TMP_DIR/$lambda.zip s3://$S3_BUCKET/apps/$APP_NAME/
done

rm -rf $TMP_DIR




