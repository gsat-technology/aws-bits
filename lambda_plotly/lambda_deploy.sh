#!/bin/bash
echo START
TMP_DIR=/tmp/deployment_packages
LAMBDA_DIR="plotly"
LAMBDA_FUNCTION=$LAMBDA_DIR


mkdir -p $TMP_DIR
cd ./lambda_code/$LAMBDA_DIR
zip -r $TMP_DIR/$LAMBDA_DIR.zip *

aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION \
    --zip-file fileb://$TMP_DIR/$LAMBDA_DIR.zip
    
