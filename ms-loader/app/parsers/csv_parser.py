import csv
import os
from datetime import datetime
from app.config.logger import logger


def transform_record(record, file_name):
    return {
        "file_name": file_name,  
        "source": record.get("source"),
        "destination": record.get("destination"),
        "starttime": datetime.fromisoformat(record.get("starttime")),
        "service": record.get("service"),
        "usage": float(record.get("usage")),
    }


def parse_csv(filepath):
    file_name = os.path.basename(filepath)
    logger.info(f"Parsing CSV file: {file_name}")
    records = []
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append(transform_record(row, file_name))
    logger.info(f"Finished parsing CSV file: {file_name}")
    return records
