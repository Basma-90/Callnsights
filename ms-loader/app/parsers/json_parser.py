import json
import os
from datetime import datetime


def transform_record(record, file_name):
    return {
        "file_name": file_name,  
        "source": record.get("source"),
        "destination": record.get("destination"),
        "starttime": datetime.fromisoformat(record.get("starttime")),
        "service": record.get("service"),
        "usage": float(record.get("usage")),
    }


def parse_json(filepath):
    file_name = os.path.basename(filepath)

    with open(filepath) as f:
        data = json.load(f)
    return [transform_record(rec, file_name) for rec in data]
