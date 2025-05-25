import os
import xml.etree.ElementTree as ET
from datetime import datetime
from app.config.logger import logger


def transform_record(record, file_name):
    """Transform XML record to standardized format"""
    return {
        "file_name": file_name,
        "source": record.get("source"),
        "destination": record.get("destination"),
        "starttime": datetime.fromisoformat(record.get("starttime")),
        "service": record.get("service"),
        "usage": float(record.get("usage")),
    }


def parse_xml(filepath):
    """Parse XML file and return list of records"""
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        file_name = os.path.basename(filepath)
        records = []

        for record in root.findall(".//record"):
            rec = {}
            for elem in record:
                rec[elem.tag] = elem.text

            try:
                transformed_record = transform_record(rec, file_name)
                records.append(transformed_record)
            except (ValueError, TypeError) as e:
                logger.error(f"Error transforming record in {file_name}: {str(e)}")
                continue

        logger.info(f"Parsed {len(records)} records from {file_name}")
        return records

    except ET.ParseError as e:
        logger.error(f"Error parsing XML file {file_name}: {str(e)}")
        return []
