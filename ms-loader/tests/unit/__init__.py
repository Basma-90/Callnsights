"""Unit Tests for CDR Loader Service

This module contains shared utilities and fixtures for unit tests.
"""

import pytest
from datetime import datetime
from pathlib import Path

# Common test data
TEST_DATA = {
    'csv_content': """source,destination,starttime,service,usage
1001,2001,2025-05-25T14:30:00,voice,12.5""",
    
    'json_content': """[{
        "source": "1001",
        "destination": "2001",
        "starttime": "2025-05-25T14:30:00",
        "service": "voice",
        "usage": 12.5
    }]""",
    
    'xml_content': """<?xml version="1.0" encoding="UTF-8"?>
<records>
    <record>
        <source>1001</source>
        <destination>2001</destination>
        <starttime>2025-05-25T14:30:00</starttime>
        <service>voice</service>
        <usage>12.5</usage>
    </record>
</records>""",
    
    'yaml_content': """
- source: "1001"
  destination: "2001"
  starttime: "2025-05-25T14:30:00"
  service: "voice"
  usage: 12.5
"""
}

# Common test record structure
TEST_RECORD = {
    "file_name": "test_file",
    "source": "1001",
    "destination": "2001",
    "starttime": datetime(2025, 5, 25, 14, 30),
    "service": "voice",
    "usage": 12.5
}

def create_test_file(tmp_path: Path, content: str, filename: str) -> Path:
    """Helper function to create test files"""
    file_path = tmp_path / filename
    file_path.write_text(content)
    return file_path