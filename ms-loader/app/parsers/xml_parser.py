import xml.etree.ElementTree as ET
import os
from datetime import datetime
from app.config.logger import logger
from app.validation.file_validator import validate_file, validate_record


def transform_record(record, file_name):
    """Transform and validate a single record."""
    try:
        return {
            "file_name": file_name,  
            "source": record.get("source"),
            "destination": record.get("destination"),
            "starttime": datetime.fromisoformat(record.get("starttime")),
            "service": record.get("service"),
            "usage": float(record.get("usage")),
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Error transforming record {record}: {str(e)}")
        return None


def parse_xml(filepath):
    """Parse XML file with validation."""
    # First validate the file itself
    if not validate_file(filepath):
        return []
    
    file_name = os.path.basename(filepath)
    logger.info(f"Parsing XML file: {file_name}")
    
    valid_records = []
    invalid_records = []
    
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        
        # Find all record elements (adjust based on your XML structure)
        record_elements = root.findall('.//record')
        
        for index, record_elem in enumerate(record_elements):
            # Convert XML element to dictionary
            record = {}
            for child in record_elem:
                record[child.tag] = child.text
            
            # Validate the raw record first
            is_valid, validation_errors = validate_record(record)
            
            if is_valid:
                # Transform the record if validation passes
                transformed_record = transform_record(record, file_name)
                if transformed_record:
                    valid_records.append(transformed_record)
                else:
                    logger.warning(f"Record {index + 1} in {file_name}: Failed to transform record")
                    invalid_records.append({
                        "index": index + 1,
                        "record": record,
                        "errors": ["Failed to transform record"]
                    })
            else:
                # Log validation errors
                logger.warning(f"Record {index + 1} in {file_name}: Validation failed - {', '.join(validation_errors)}")
                invalid_records.append({
                    "index": index + 1,
                    "record": record,
                    "errors": validation_errors
                })
    
    except ET.ParseError as e:
        logger.error(f"XML parse error in {file_name}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error parsing XML file {file_name}: {str(e)}")
        return []
    
    logger.info(f"Finished parsing XML file: {file_name}. Valid: {len(valid_records)}, Invalid: {len(invalid_records)}")
    

    if invalid_records:
        logger.warning(f"Invalid records in {file_name}:")
        for invalid in invalid_records[:5]:
            logger.warning(f"  Record {invalid['index']}: {', '.join(invalid['errors'])}")
        if len(invalid_records) > 5:
            logger.warning(f"  ... and {len(invalid_records) - 5} more invalid records")
    
    return valid_records