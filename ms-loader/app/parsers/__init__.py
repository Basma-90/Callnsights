import os
from app.config.logger import logger
from .csv_parser import parse_csv
from .json_parser import parse_json
from .xml_parser import parse_xml
from .yaml_parser import parse_yaml



def parse_all_files(directory):
    """
    Parse all supported files in the directory with validation.
    Returns a tuple of (valid_records, validation_summary)
    """
    if not os.path.exists(directory):
        logger.error(f"Directory does not exist: {directory}")
        return [], {"error": "Directory not found", "files_processed": 0}
    
    valid_records = []
    validation_summary = {
        "files_processed": 0,
        "valid_files": 0,
        "invalid_files": 0,
        "total_valid_records": 0,
        "files_with_errors": [],
        "processing_errors": []
    }
    
    supported_extensions = ['.csv', '.json', '.xml', '.yaml', '.yml']
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue
        
        _, ext = os.path.splitext(filename.lower())
        if ext not in supported_extensions:
            continue
            
        validation_summary["files_processed"] += 1
        records = []
        
        try:
            if ext == '.csv':
                records = parse_csv(filepath)
            elif ext == '.json':
                records = parse_json(filepath)
            elif ext == '.xml':
                records = parse_xml(filepath)
            elif ext in ['.yaml', '.yml']:
                records = parse_yaml(filepath)
            
            if records:
                validation_summary["valid_files"] += 1
                validation_summary["total_valid_records"] += len(records)
                valid_records.extend(records)
                logger.info(f"Successfully processed {filename}: {len(records)} valid records")
            else:
                validation_summary["invalid_files"] += 1
                validation_summary["files_with_errors"].append({
                    "filename": filename,
                    "error": "No valid records found"
                })
                logger.warning(f"No valid records found in {filename}")
                
        except Exception as e:
            validation_summary["invalid_files"] += 1
            error_msg = f"Processing error: {str(e)}"
            validation_summary["processing_errors"].append({
                "filename": filename,
                "error": error_msg
            })
            logger.error(f"Error processing file {filename}: {str(e)}")
    

    logger.info(f"Parsing complete - Files processed: {validation_summary['files_processed']}, "
                f"Valid files: {validation_summary['valid_files']}, "
                f"Invalid files: {validation_summary['invalid_files']}, "
                f"Total valid records: {validation_summary['total_valid_records']}")
    
    return valid_records, validation_summary