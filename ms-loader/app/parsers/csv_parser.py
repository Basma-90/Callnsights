import csv
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


def parse_csv(filepath):
    """Parse CSV file with validation."""
    if not validate_file(filepath):
        return []
    
    file_name = os.path.basename(filepath)
    logger.info(f"Parsing CSV file: {file_name}")
    
    valid_records = []
    invalid_records = []
    row_number = 0
    
    try:
        with open(filepath, newline="", encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                row_number += 1
                
                # Validate the raw record first
                is_valid, validation_errors = validate_record(row)
                
                if is_valid:
                    # Transform the record if validation passes
                    transformed_record = transform_record(row, file_name)
                    if transformed_record:
                        valid_records.append(transformed_record)
                    else:
                        logger.warning(f"Row {row_number} in {file_name}: Failed to transform record")
                        invalid_records.append({
                            "row": row_number,
                            "record": row,
                            "errors": ["Failed to transform record"]
                        })
                else:
                    # Log validation errors
                    logger.warning(f"Row {row_number} in {file_name}: Validation failed - {', '.join(validation_errors)}")
                    invalid_records.append({
                        "row": row_number,
                        "record": row,
                        "errors": validation_errors
                    })
    
    except Exception as e:
        logger.error(f"Error parsing CSV file {file_name}: {str(e)}")
        return []
    
    logger.info(f"Finished parsing CSV file: {file_name}. Valid: {len(valid_records)}, Invalid: {len(invalid_records)}")
    
    # Log summary of invalid records
    if invalid_records:
        logger.warning(f"Invalid records in {file_name}:")
        for invalid in invalid_records[:5]:
            logger.warning(f"  Row {invalid['row']}: {', '.join(invalid['errors'])}")
        if len(invalid_records) > 5:
            logger.warning(f"  ... and {len(invalid_records) - 5} more invalid records")
    
    return valid_records