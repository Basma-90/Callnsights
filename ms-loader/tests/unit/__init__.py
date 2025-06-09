"""Unit Tests for CDR Loader Service

This module contains shared utilities and fixtures for unit tests.
"""

import pytest
from datetime import datetime
from pathlib import Path

# Common test data with valid CDR records
TEST_DATA = {
    'csv_content': """source,destination,starttime,service,usage
+1234567890,+9876543210,2024-01-15T10:30:00,VOICE,15.5
+1234567891,+9876543211,2024-01-15T11:45:30,SMS,1
+1234567892,https://www.example.com,2024-01-15T12:15:45,DATA,250.75""",
    
    'json_content': """[{
        "source": "+1234567890",
        "destination": "+9876543210",
        "starttime": "2024-01-15T10:30:00",
        "service": "VOICE",
        "usage": 15.5
    }, {
        "source": "+1234567891",
        "destination": "+9876543211",
        "starttime": "2024-01-15T11:45:30",
        "service": "SMS",
        "usage": 1
    }]""",
    
    'xml_content': """<?xml version="1.0" encoding="UTF-8"?>
<records>
    <record>
        <source>+1234567890</source>
        <destination>+9876543210</destination>
        <starttime>2024-01-15T10:30:00</starttime>
        <service>VOICE</service>
        <usage>15.5</usage>
    </record>
</records>""",
    
    'yaml_content': """
- source: "+1234567890"
  destination: "+9876543210"
  starttime: "2024-01-15T10:30:00"
  service: "VOICE"
  usage: 15.5
- source: "+1234567891"
  destination: "https://api.example.com"
  starttime: "2024-01-15T12:15:45"
  service: "DATA"
  usage: 125.0
""",

    # Invalid test data for validation testing
    'invalid_csv_content': """source,destination,starttime,service,usage
invalid-phone,+9876543210,2024-01-15T10:30:00,VOICE,15.5
+1234567891,,2024-01-15T11:45:30,SMS,1
+1234567892,https://www.example.com,invalid-date,DATA,250.75""",

    'empty_csv_content': """source,destination,starttime,service,usage""",
}

# Common test record structure
TEST_RECORD = {
    "file_name": "test_file",
    "source": "+1234567890",
    "destination": "+9876543210",
    "starttime": datetime(2024, 1, 15, 10, 30),
    "service": "VOICE",
    "usage": 15.5
}

def create_test_file(tmp_path: Path, content: str, filename: str) -> Path:
    """Helper function to create test files"""
    file_path = tmp_path / filename
    file_path.write_text(content)
    return file_path