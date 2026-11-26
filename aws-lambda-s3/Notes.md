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