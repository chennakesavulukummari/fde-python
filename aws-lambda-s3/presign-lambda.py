import base64
import json
import os
import re
import time
import uuid

import boto3
from botocore.config import Config

BUCKET = os.environ["BUCKET_NAME"]
PREFIX = os.environ.get("UPLOAD_PREFIX", "uploads/")
MAX_BYTES = int(os.environ.get("MAX_BYTES", 10 * 1024 * 1024))
URL_EXPIRY_SECONDS = 300

# Optional allow-list. Leave empty to accept any content type.
ALLOWED_TYPES = [t for t in os.environ.get("ALLOWED_TYPES", "").split(",") if t]

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))


def _response(status, body):
    # CORS headers come from the Function URL CORS settings, not from this code.
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def _safe_name(name):
    name = os.path.basename(name)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    return name[:100] or "file"


def lambda_handler(event, context):
    try:
        raw = event.get("body") or "{}"
        if event.get("isBase64Encoded"):
            raw = base64.b64decode(raw).decode("utf-8")
        data = json.loads(raw)

        file_name = _safe_name(data["fileName"])
        content_type = data.get("contentType") or "application/octet-stream"
        size = int(data.get("size", 0))
    except (KeyError, ValueError, json.JSONDecodeError):
        return _response(400, {"error": "Invalid request body"})

    if size <= 0 or size > MAX_BYTES:
        return _response(400, {"error": f"File must be between 1 byte and {MAX_BYTES} bytes"})

    if ALLOWED_TYPES and content_type not in ALLOWED_TYPES:
        return _response(400, {"error": f"Content type {content_type} is not allowed"})

    key = f"{PREFIX}{int(time.time())}-{uuid.uuid4().hex[:8]}-{file_name}"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={"Bucket": BUCKET, "Key": key, "ContentType": content_type},
        ExpiresIn=URL_EXPIRY_SECONDS,
    )

    return _response(200, {"uploadUrl": upload_url, "key": key})