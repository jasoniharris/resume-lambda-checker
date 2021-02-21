#!/usr/bin/env bash

ROLE=`aws cloudformation describe-stacks --stack-name react-resume-amplify --query "Stacks[0].Outputs[?OutputKey=='IAMLambdaServiceRole'].OutputValue" --output text --profile jh-developer --region eu-west-2`
SNS_TOPIC=`aws cloudformation describe-stacks --stack-name react-resume-amplify --query "Stacks[0].Outputs[?OutputKey=='resumeCheckerSNSTopic'].OutputValue" --output text --profile jh-developer --region eu-west-2`
S3_BUCKET=`aws cloudformation describe-stacks --stack-name react-resume-amplify --query "Stacks[0].Outputs[?OutputKey=='resumeS3Bucket'].OutputValue" --output text --profile jh-developer --region eu-west-2`

echo "ROLE is ${ROLE}"
echo "SNS is ${SNS_TOPIC}"
echo "S3_BUCKET is ${S3_BUCKET}"

sam package \
  --template-file template.yml \
  --output-template-file package.yml \
  --s3-bucket ${S3_BUCKET} \
  --profile jh-developer

sam deploy \
  --template-file package.yml \
  --stack-name resume-checker \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides ROLE=$ROLE SNSTOPIC=$SNS_TOPIC \
  --profile jh-developer \
  --region eu-west-2