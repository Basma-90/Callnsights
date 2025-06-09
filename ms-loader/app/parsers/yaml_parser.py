import os
import yaml
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
            "service": record.get("service").upper(),  # Normalize service type
            "usage": float(record.get("usage")),
        }
    except (ValueError, TypeError) as e:
        logger.error(f"Error transforming record {record}: {str(e)}")
        return None


def parse_yaml(filepath):
    """Parse YAML file with validation."""
    # First validate the file itself
    if not validate_file(filepath):
        return []
    
    file_name = os.path.basename(filepath)
    logger.info(f"Parsing YAML file: {file_name}")
    
    valid_records = []
    invalid_records = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as yamlfile:
            data = yaml.safe_load(yamlfile)
            
            # Handle different YAML structures
            if isinstance(data, list):
                records_list = data
            elif isinstance(data, dict) and 'records' in data:
                records_list = data['records']
            else:
                logger.error(f"Invalid YAML structure in {file_name}. Expected list or object with 'records' key")
                return []
            
            for index, record in enumerate(records_list):
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
    
    except yaml.YAMLError as e:
        logger.error(f"YAML parse error in {file_name}: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error parsing YAML file {file_name}: {str(e)}")
        return []
    
    logger.info(f"Finished parsing YAML file: {file_name}. Valid: {len(valid_records)}, Invalid: {len(invalid_records)}")
    
    if invalid_records:
        logger.warning(f"Invalid records in {file_name}:")
        for invalid in invalid_records[:5]: 
            logger.warning(f"  Record {invalid['index']}: {', '.join(invalid['errors'])}")
        if len(invalid_records) > 5:
            logger.warning(f"  ... and {len(invalid_records) - 5} more invalid records")
    
    return valid_records