#!/bin/bash

while true
do
    aws lambda invoke --function-name timePutObject --payload '{"infiles": ["files/1MB.file", "files/2MB.file", "files/4MB.file", "files/8MB.file", "files/16MB.file" ]}' outfile.txt && cat outfile.txt
done



