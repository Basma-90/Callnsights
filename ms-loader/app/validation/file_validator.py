from datetime import datetime
import os
import re
from app.config.logger import logger
import urllib.parse

ALLOWED_EXTENSIONS = {'.csv', '.json', '.xml', '.yaml'}
REQUIRED_FIELDS = ['source', 'destination', 'starttime', 'service', 'usage']
SERVICE_TYPES = ['VOICE', 'SMS', 'DATA']
PHONE_PATTERN = re.compile(r'^\+?[1-9]\d{1,14}$')  
URL_PATTERN = re.compile(r'^(http|https)://[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}(:[0-9]{1,5})?(\/.*)?$')

def validate_file(filepath):
    """Validate if a file exists and has an allowed extension."""
    if not os.path.exists(filepath):
        logger.error(f"File does not exist: {filepath}")
        return False
    
    _, ext = os.path.splitext(filepath)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        logger.error(f"Unsupported file type: {ext}")
        return False
    
    if os.path.getsize(filepath) == 0:
        logger.error(f"File is empty: {filepath}")
        return False
    
    return True

def validate_record(record):
    """Validate a single CDR record."""
    errors = []
    
    for field in REQUIRED_FIELDS:
        if field not in record or record[field] is None or record[field] == '':
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    if not PHONE_PATTERN.match(record['source']):
        errors.append(f"Invalid source format: {record['source']}")

    if record['service'].upper() not in SERVICE_TYPES:
        errors.append(f"Invalid service type: {record['service']}. Must be one of: {', '.join(SERVICE_TYPES)}")
    else:
        service = record['service'].upper()
        
        if service in ['VOICE', 'SMS']:
            if not PHONE_PATTERN.match(record['destination']):
                errors.append(f"Invalid destination format for {service}: {record['destination']}. Should be a phone number.")
        elif service == 'DATA':
            try:
                if not URL_PATTERN.match(record['destination']):
                    parsed_url = urllib.parse.urlparse(record['destination'])
                    if not all([parsed_url.scheme, parsed_url.netloc]):
                        errors.append(f"Invalid URL format for DATA service: {record['destination']}")
            except ValueError:
                errors.append(f"Invalid URL format for DATA service: {record['destination']}")
    
        try:
            usage = float(record['usage'])
            
            if usage < 0:
                errors.append(f"Usage must be positive: {usage}")
            
            if service == 'VOICE':
                if usage > 1440:  
                    errors.append(f"Voice call duration ({usage} minutes) exceeds reasonable limit")
                    
            elif service == 'DATA':
                if usage > 100000:  
                    errors.append(f"Data usage ({usage} MB) exceeds reasonable limit")
                    
            elif service == 'SMS':
                if usage != 1:
                    errors.append(f"SMS usage must be exactly 1, got: {usage}")
        except (ValueError, TypeError):
            errors.append(f"Usage must be a number: {record['usage']}")
    

    try:
        if isinstance(record['starttime'], str):
            dt = datetime.fromisoformat(record['starttime'].replace('Z', '+00:00'))
            
            if dt > datetime.now():
                errors.append(f"StartTime cannot be in the future: {record['starttime']}")
            
            ten_years_ago = datetime.now().replace(year=datetime.now().year - 10)
            if dt < ten_years_ago:
                errors.append(f"StartTime is unreasonably old: {record['starttime']}")
    except (ValueError, TypeError):
        errors.append(f"Invalid datetime format: {record['starttime']}")
    
    if 'source' in record and 'destination' in record and record['source'] == record['destination']:
        if record.get('service', '').upper() in ['VOICE', 'SMS']:
            errors.append(f"Source and destination cannot be identical for {record['service']}")
    
    return len(errors) == 0, errors

def get_service_specific_validation_message(service):
    """Return service-specific validation guidelines."""
    if service == 'VOICE':
        return "VOICE records require: phone number source, phone number destination, usage in minutes"
    elif service == 'SMS':
        return "SMS records require: phone number source, phone number destination, usage must be 1"
    elif service == 'DATA':
        return "DATA records require: phone number source, URL destination, usage in megabytes (MB)"
    else:
        return f"Unknown service type: {service}"