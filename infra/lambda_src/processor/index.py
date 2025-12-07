import json
import os
from datetime import datetime
from typing import Any, Dict

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Stub processor that logs the incoming S3 object reference and writes a placeholder
    record to DynamoDB. Extend this to call Textract/Comprehend and apply fraud rules.
    """
    bucket = event.get("bucket")
    key = event.get("key")

    record = {
        "pk": f"receipt#{key or 'unknown'}",
        "bucket": bucket or "unknown",
        "object_key": key or "unknown",
        "status": "STUB_PROCESSED",
        "processed_at": datetime.utcnow().isoformat(),
        "notes": "Replace with real OCR/PII/fraud logic",
    }

    table.put_item(Item=record)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Stub processed", "record": record}),
    }
