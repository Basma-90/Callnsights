import pytest
from app.validation.file_validator import validate_file, validate_record, get_service_specific_validation_message
from tests.unit import create_test_file


def test_validate_file_exists(tmp_path):
    """Test file validation for existing file"""
    file_path = create_test_file(tmp_path, "source,destination\n+123,+456", 'test.csv')
    assert validate_file(str(file_path)) == True


def test_validate_file_nonexistent():
    """Test file validation for non-existent file"""
    assert validate_file('/nonexistent/file.csv') == False


def test_validate_file_wrong_extension(tmp_path):
    """Test file validation for unsupported extension"""
    file_path = create_test_file(tmp_path, "content", 'test.txt')
    assert validate_file(str(file_path)) == False


def test_validate_file_empty(tmp_path):
    """Test file validation for empty file"""
    file_path = create_test_file(tmp_path, "", 'empty.csv')
    assert validate_file(str(file_path)) == False


def test_validate_record_valid_voice():
    """Test validation of valid VOICE record"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "VOICE",
        "usage": "15.5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == True
    assert len(errors) == 0


def test_validate_record_valid_sms():
    """Test validation of valid SMS record"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "SMS",
        "usage": "1"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == True
    assert len(errors) == 0


def test_validate_record_valid_data():
    """Test validation of valid DATA record"""
    record = {
        "source": "+1234567890",
        "destination": "https://www.example.com",
        "starttime": "2024-01-15T10:30:00",
        "service": "DATA",
        "usage": "250.75"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == True
    assert len(errors) == 0


def test_validate_record_missing_fields():
    """Test validation of record with missing fields"""
    record = {"source": "+1234567890"}
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert len(errors) == 4 


def test_validate_record_invalid_phone_source():
    """Test validation of record with invalid phone source"""
    record = {
        "source": "invalid-phone",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "VOICE",
        "usage": "15.5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("Invalid source format" in error for error in errors)


def test_validate_record_invalid_service_type():
    """Test validation of record with invalid service type"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "INVALID",
        "usage": "15.5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("Invalid service type" in error for error in errors)


def test_validate_record_sms_wrong_usage():
    """Test validation of SMS record with usage != 1"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "SMS",
        "usage": "5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("SMS usage must be exactly 1" in error for error in errors)


def test_validate_record_data_invalid_url():
    """Test validation of DATA record with invalid URL"""
    record = {
        "source": "+1234567890",
        "destination": "not-a-url",
        "starttime": "2024-01-15T10:30:00",
        "service": "DATA",
        "usage": "250.75"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("Invalid URL format" in error for error in errors)


def test_validate_record_negative_usage():
    """Test validation of record with negative usage"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "VOICE",
        "usage": "-15.5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("Usage must be positive" in error for error in errors)


def test_validate_record_invalid_datetime():
    """Test validation of record with invalid datetime"""
    record = {
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "invalid-date",
        "service": "VOICE",
        "usage": "15.5"
    }
    is_valid, errors = validate_record(record)
    assert is_valid == False
    assert any("Invalid datetime format" in error for error in errors)


def test_get_service_specific_validation_message():
    """Test service-specific validation messages"""
    voice_msg = get_service_specific_validation_message("VOICE")
    sms_msg = get_service_specific_validation_message("SMS")
    data_msg = get_service_specific_validation_message("DATA")
    unknown_msg = get_service_specific_validation_message("UNKNOWN")
    
    assert "phone number" in voice_msg and "minutes" in voice_msg
    assert "phone number" in sms_msg and "usage must be 1" in sms_msg
    assert "URL" in data_msg and "megabytes" in data_msg
    assert "Unknown service type" in unknown_msg