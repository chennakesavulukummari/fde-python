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
