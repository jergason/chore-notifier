#! /bin/bash

set -e
set -x


rm -rf function.zip
(
    cd package
    zip -r9q ../function.zip .
)
zip -g function.zip function.py
aws lambda update-function-code --function-name chore-list --zip-file fileb://function.zip
