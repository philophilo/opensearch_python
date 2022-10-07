#! /bin/sh

pwd
mkdir -p ~/.aws
echo "[default]" > ~/.aws/credentials
echo "aws_access_key_id = ${ACCESS_KEY}" >>  ~/.aws/credentials
echo "aws_secret_access_key = ${SECRET_ACCESS_KEY}" >> ~/.aws/credentials

echo "[default]" > ~/.aws/config
echo "region = ${REGION}" >> ~/.aws/config
echo "output = json" >> ~/.aws/config

python Log_Producer_Desktop.py