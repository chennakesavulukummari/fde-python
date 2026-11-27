# Python + AWS Lambda + S3: Object Upload Notification

# Project: S3 Object Upload Notification System

Business scenario: 

Imagine Cloud Binary receives hundreds of files from customers every day. 

Whenever a customer uploads a file to an Amazon S3 bucket, the system should automatically detect the upload, process the file metadata, and send a notification.

# Workflow
1. User uploads a file
   
   Customer uploads invoice.pdf to Amazon S3.

2. S3 generates an event
   
   S3 detects the ObjectCreated event.

3. AWS Lambda executes
   
   Lambda invokes a Python function automatically.

4. Python processes the event
   
   Extract bucket name, file name, file size and upload details.

5. Send notification
   
   Amazon SNS sends an email notification to the operations team.

# 1. AWS services required
AWS service	            Responsibility
Amazon S3	            Store uploaded files
AWS Lambda	            Execute Python code
Amazon SNS	            Send email notifications
AWS IAM	                Manage permissions
Amazon CloudWatch	    Store Lambda execution logs

# Architecture

# The event flow:

Customer
   |
   | Upload invoice.pdf
   v
Amazon S3 Bucket
   |
   | ObjectCreated Event
   v
AWS Lambda
   |
   | Python Function
   | Extract Object Metadata
   v
Amazon SNS
   |
   | Email Notification
   v
Operations Team

# 3. Create an S3 bucket
Go to AWS Console:
1. Open Amazon S3.
2. Click Create bucket.
3. Bucket name: cloudbinary-fde-upload-demo
4. Select your AWS region.
5. Keep Block Public Access enabled.
6. Create bucket.

We will use this bucket to receive uploaded files.

# 4. Create an SNS topic
Open Amazon SNS.
1. Navigate to Topics.
2. Click Create topic.
3. Type: Standard.
4. Name: cloudbinary-upload-notifications.
5. Create topic.
6. Copy the SNS Topic ARN.

Example: arn:aws:sns:us-east-1:225989338000:cloudbinary-upload-notifications

Next, create an email subscription:
- Protocol: Email
- Endpoint: Your email address
- Confirm the subscription from your inbox.

Important: Until you confirm the subscription, SNS will not deliver the email.

# 5. Create the Lambda function
Open AWS Lambda.
1. Click Create function.
2. Select Author from scratch.
3. Function name: cloudbinary-s3-upload-notifier
4. Runtime: Python 3.12 or a currently supported Python runtime.
5. Architecture: x86_64.
6. Create function.

# 6. Understand the Python Lambda function
Before writing the complete code, let's understand how AWS Lambda works.

AWS invokes a Python handler function whenever an event arrives.

```
def lambda_handler(event, context):

    print("S3 Upload Event Received")

    return {
        "statusCode": 200,
        "body": "File uploaded successfully"
    }
```

Two important parameters:
- event: Contains information about what triggered Lambda.
- context: Contains runtime information about the Lambda execution.

# 7. Write the Python Lambda code
Now let's use Python functions to implement the business logic.

Our Lambda will perform three operations:
1. Extract S3 upload information.
2. Prepare a notification message.
3. Publish the notification to SNS.
   
# Lambda function code:

```

import json
import os
import urllib.parse
import boto3

# Initialize AWS SNS client
sns = boto3.client("sns")

SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


# Function 1: Extract S3 object information
def extract_file_details(record):

    bucket_name = record["s3"]["bucket"]["name"]

    object_key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )

    file_size = record["s3"]["object"]["size"]

    event_name = record["eventName"]

    return {
        "bucket": bucket_name,
        "file_name": object_key,
        "file_size": file_size,
        "event": event_name
    }


# Function 2: Generate notification message
def generate_notification(details):

    message = f"""
    Cloud Binary - S3 Upload Notification

    Event: {details['event']}
    Bucket: {details['bucket']}
    File: {details['file_name']}
    File Size: {details['file_size']} bytes

    Status: Upload Detected Successfully
    """

    return message


# Function 3: Send notification using SNS
def send_notification(message):

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="New S3 Object Uploaded",
        Message=message
    )

    return response["MessageId"]


# Main Lambda handler
def lambda_handler(event, context):

    print("Received S3 Event")

    results = []

    for record in event["Records"]:

        # Extract object information
        details = extract_file_details(record)

        print("File Details:", json.dumps(details))

        # Generate notification
        message = generate_notification(details)

        # Send SNS notification
        message_id = send_notification(message)

        results.append({
            "file": details["file_name"],
            "message_id": message_id,
            "status": "Notification Sent"
        })

    return {
        "statusCode": 200,
        "body": json.dumps(results)
    }


```

Status: Failed
Test Event Name: Test-01

Response:
{
  "errorMessage": "'Records'",
  "errorType": "KeyError",
  "requestId": "4d0bba70-1a14-4a2f-821e-98f8b553a395",
  "stackTrace": [
    "  File \"/var/task/lambda_function.py\", line 69, in lambda_handler\n    for record in event[\"Records\"]:\n"
  ]
}

The area below shows the last 4 KB of the execution log.

Function Logs:
START RequestId: 4d0bba70-1a14-4a2f-821e-98f8b553a395 Version: $LATEST
Received S3 Event
[ERROR] KeyError: 'Records'
Traceback (most recent call last):
  File "/var/task/lambda_function.py", line 69, in lambda_handler
    for record in event["Records"]:
END RequestId: 4d0bba70-1a14-4a2f-821e-98f8b553a395
REPORT RequestId: 4d0bba70-1a14-4a2f-821e-98f8b553a395	Duration: 9.86 ms	Billed Duration: 458 ms	Memory Size: 128 MB	Max Memory Used: 87 MB	Init Duration: 447.81 ms

Request ID: 4d0bba70-1a14-4a2f-821e-98f8b553a395


```
{
  "Records": [
    {
      "eventName": "ObjectCreated:Put",
      "s3": {
        "bucket": {
          "name": "cloudbinary-fde-upload-demo"
        },
        "object": {
          "key": "invoice.pdf",
          "size": 102400
        }
      }
    }
  ]
}
```

Status: Failed
Test Event Name: Test-01

Response:
{
  "errorMessage": "An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:sts::225989338000:assumed-role/cloudbinary-s3-upload-notifier-role-fyb9z3m8/cloudbinary-s3-upload-notifier is not authorized to perform: SNS:Publish on resource: arn:aws:sns:us-east-1:225989338000:cloudbinary-upload-notifications because no identity-based policy allows the SNS:Publish action",
  "errorType": "AuthorizationErrorException",
  "requestId": "2ad3a2db-b72f-4b49-a4f2-92b03ed3876c",
  "stackTrace": [
    "  File \"/var/task/lambda_function.py\", line 80, in lambda_handler\n    message_id = send_notification(message)\n",
    "  File \"/var/task/lambda_function.py\", line 53, in send_notification\n    response = sns.publish(\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/client.py\", line 606, in _api_call\n    return self._make_api_call(operation_name, kwargs)\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/context.py\", line 123, in wrapper\n    return func(*args, **kwargs)\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/client.py\", line 1094, in _make_api_call\n    raise error_class(parsed_response, operation_name)\n"
  ]
}

The area below shows the last 4 KB of the execution log.

Function Logs:
START RequestId: 2ad3a2db-b72f-4b49-a4f2-92b03ed3876c Version: $LATEST
Received S3 Event
File Details: {"bucket": "cloudbinary-fde-upload-demo", "file_name": "invoice.pdf", "file_size": 102400, "event": "ObjectCreated:Put"}
[ERROR] AuthorizationErrorException: An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:sts::225989338000:assumed-role/cloudbinary-s3-upload-notifier-role-fyb9z3m8/cloudbinary-s3-upload-notifier is not authorized to perform: SNS:Publish on resource: arn:aws:sns:us-east-1:225989338000:cloudbinary-upload-notifications because no identity-based policy allows the SNS:Publish action
Traceback (most recent call last):
  File "/var/task/lambda_function.py", line 80, in lambda_handler
    message_id = send_notification(message)
  File "/var/task/lambda_function.py", line 53, in send_notification
    response = sns.publish(
  File "/var/lang/lib/python3.13/site-packages/botocore/client.py", line 606, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/var/lang/lib/python3.13/site-packages/botocore/context.py", line 123, in wrapper
    return func(*args, **kwargs)
  File "/var/lang/lib/python3.13/site-packages/botocore/client.py", line 1094, in _make_api_call
    raise error_class(parsed_response, operation_name)
END RequestId: 2ad3a2db-b72f-4b49-a4f2-92b03ed3876c
REPORT RequestId: 2ad3a2db-b72f-4b49-a4f2-92b03ed3876c	Duration: 386.90 ms	Billed Duration: 387 ms	Memory Size: 128 MB	Max Memory Used: 89 MB

Request ID: 2ad3a2db-b72f-4b49-a4f2-92b03ed3876c


Status: Failed
Test Event Name: Test-02

Response:
{
  "errorMessage": "An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:sts::225989338000:assumed-role/cloudbinary-s3-upload-notifier-role-fyb9z3m8/cloudbinary-s3-upload-notifier is not authorized to perform: SNS:Publish on resource: arn:aws:sns:us-east-1:225989338000:cloudbinary-upload-notifications because no identity-based policy allows the SNS:Publish action",
  "errorType": "AuthorizationErrorException",
  "requestId": "a91b73ff-49a8-404c-aa68-5c3ebabebad7",
  "stackTrace": [
    "  File \"/var/task/lambda_function.py\", line 80, in lambda_handler\n    message_id = send_notification(message)\n",
    "  File \"/var/task/lambda_function.py\", line 53, in send_notification\n    response = sns.publish(\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/client.py\", line 606, in _api_call\n    return self._make_api_call(operation_name, kwargs)\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/context.py\", line 123, in wrapper\n    return func(*args, **kwargs)\n",
    "  File \"/var/lang/lib/python3.13/site-packages/botocore/client.py\", line 1094, in _make_api_call\n    raise error_class(parsed_response, operation_name)\n"
  ]
}

The area below shows the last 4 KB of the execution log.

Function Logs:
START RequestId: a91b73ff-49a8-404c-aa68-5c3ebabebad7 Version: $LATEST
Received S3 Event
File Details: {"bucket": "cloudbinary-fde-upload-demo", "file_name": "invoice.pdf", "file_size": 102400, "event": "ObjectCreated:Put"}
[ERROR] AuthorizationErrorException: An error occurred (AuthorizationError) when calling the Publish operation: User: arn:aws:sts::225989338000:assumed-role/cloudbinary-s3-upload-notifier-role-fyb9z3m8/cloudbinary-s3-upload-notifier is not authorized to perform: SNS:Publish on resource: arn:aws:sns:us-east-1:225989338000:cloudbinary-upload-notifications because no identity-based policy allows the SNS:Publish action
Traceback (most recent call last):
  File "/var/task/lambda_function.py", line 80, in lambda_handler
    message_id = send_notification(message)
  File "/var/task/lambda_function.py", line 53, in send_notification
    response = sns.publish(
  File "/var/lang/lib/python3.13/site-packages/botocore/client.py", line 606, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/var/lang/lib/python3.13/site-packages/botocore/context.py", line 123, in wrapper
    return func(*args, **kwargs)
  File "/var/lang/lib/python3.13/site-packages/botocore/client.py", line 1094, in _make_api_call
    raise error_class(parsed_response, operation_name)
END RequestId: a91b73ff-49a8-404c-aa68-5c3ebabebad7
REPORT RequestId: a91b73ff-49a8-404c-aa68-5c3ebabebad7	Duration: 203.57 ms	Billed Duration: 204 ms	Memory Size: 128 MB	Max Memory Used: 90 MB

Request ID: a91b73ff-49a8-404c-aa68-5c3ebabebad7



Status: Succeeded
Test Event Name: Test-02

Response:
{
  "statusCode": 200,
  "body": "[{\"file\": \"invoice.pdf\", \"message_id\": \"d9de12eb-4365-5425-bbfd-7168f3dcde2f\", \"status\": \"Notification Sent\"}]"
}

The area below shows the last 4 KB of the execution log.

Function Logs:
START RequestId: 5a8748f9-f0d7-41b7-8e23-b59bc1d41c7f Version: $LATEST
Received S3 Event
File Details: {"bucket": "cloudbinary-fde-upload-demo", "file_name": "invoice.pdf", "file_size": 102400, "event": "ObjectCreated:Put"}
END RequestId: 5a8748f9-f0d7-41b7-8e23-b59bc1d41c7f
REPORT RequestId: 5a8748f9-f0d7-41b7-8e23-b59bc1d41c7f	Duration: 256.28 ms	Billed Duration: 257 ms	Memory Size: 128 MB	Max Memory Used: 90 MB

Request ID: 5a8748f9-f0d7-41b7-8e23-b59bc1d41c7f


