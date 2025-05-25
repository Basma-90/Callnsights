import os
from datetime import datetime

import yaml


def transform_record(record, file_name):
    """Transform a record with filename included"""
    return {
        "file_name": file_name, 
        "source": record.get("source"),
        "destination": record.get("destination"),
        "starttime": datetime.fromisoformat(record.get("starttime")),
        "service": record.get("service"),
        "usage": float(record.get("usage")),
    }


def parse_yaml(filepath):
    """Parse YAML file and return records with filename"""
    file_name = os.path.basename(filepath)

    with open(filepath) as f:
        data = yaml.safe_load(f)

    if not data:
        return []

    records = []
    for rec in data:
        records.append(transform_record(rec, file_name))

    return records
