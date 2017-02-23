#!/bin/bash
echo START
STACK_NAME=$1
TMP_DIR=/tmp/deployment_packages
LAMBDA_DIR="imageCRUD"
LAMBDA_FUNCTION="$STACK_NAME"_$LAMBDA_DIR


mkdir -p $TMP_DIR
cd ./lambda_code/$LAMBDA_DIR
zip -r $TMP_DIR/$LAMBDA_DIR.zip *

aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION \
    --zip-file fileb://$TMP_DIR/$LAMBDA_DIR.zip
    
