import os
import pytest
from app.parsers import parse_all_files
from app.parsers.csv_parser import parse_csv
from app.parsers.json_parser import parse_json
from app.parsers.xml_parser import parse_xml
from app.parsers.yaml_parser import parse_yaml
from tests.unit import TEST_DATA, TEST_RECORD, create_test_file


def test_parse_csv_valid(tmp_path):
    """Test parsing valid CSV file"""
    file_path = create_test_file(tmp_path, TEST_DATA['csv_content'], 'test.csv')
    
    records = parse_csv(str(file_path))
    assert len(records) == 3  
    assert records[0]['source'] == TEST_RECORD['source']
    assert records[0]['service'] == 'VOICE'
    assert records[1]['service'] == 'SMS'
    assert records[1]['usage'] == 1  
    assert records[2]['service'] == 'DATA'


def test_parse_csv_invalid(tmp_path):
    """Test parsing CSV file with invalid records"""
    file_path = create_test_file(tmp_path, TEST_DATA['invalid_csv_content'], 'invalid.csv')
    
    records = parse_csv(str(file_path))
    assert len(records) == 0


def test_parse_csv_empty(tmp_path):
    """Test parsing empty CSV file"""
    file_path = create_test_file(tmp_path, TEST_DATA['empty_csv_content'], 'empty.csv')
    
    records = parse_csv(str(file_path))
    assert len(records) == 0


def test_parse_json_valid(tmp_path):
    """Test parsing valid JSON file"""
    file_path = create_test_file(tmp_path, TEST_DATA['json_content'], 'test.json')

    records = parse_json(str(file_path))
    assert len(records) == 2 
    assert records[0]['source'] == TEST_RECORD['source']
    assert records[0]['service'] == 'VOICE'
    assert records[1]['service'] == 'SMS'


def test_parse_xml_valid(tmp_path):
    """Test parsing valid XML file"""
    file_path = create_test_file(tmp_path, TEST_DATA['xml_content'], 'test.xml')
    
    records = parse_xml(str(file_path))
    assert len(records) == 1
    assert records[0]['source'] == TEST_RECORD['source']
    assert records[0]['service'] == 'VOICE'


def test_parse_yaml_valid(tmp_path):
    """Test parsing valid YAML file"""
    file_path = create_test_file(tmp_path, TEST_DATA['yaml_content'], 'test.yaml')
    
    records = parse_yaml(str(file_path))
    assert len(records) == 2
    assert records[0]['source'] == TEST_RECORD['source']
    assert records[0]['service'] == 'VOICE'
    assert records[1]['service'] == 'DATA'


def test_parse_all_files_valid(tmp_path):
    """Test parsing all valid files in directory"""
    create_test_file(tmp_path, TEST_DATA['csv_content'], 'test.csv')
    create_test_file(tmp_path, TEST_DATA['json_content'], 'test.json')
    create_test_file(tmp_path, TEST_DATA['xml_content'], 'test.xml')
    create_test_file(tmp_path, TEST_DATA['yaml_content'], 'test.yaml')
    
    records, validation_summary = parse_all_files(str(tmp_path))
    
    assert len(records) == 8
    assert validation_summary['files_processed'] == 4
    assert validation_summary['valid_files'] == 4
    assert validation_summary['invalid_files'] == 0
    assert validation_summary['total_valid_records'] == 8


def test_parse_all_files_mixed_valid_invalid(tmp_path):
    """Test parsing directory with both valid and invalid files"""
    create_test_file(tmp_path, TEST_DATA['csv_content'], 'valid.csv')
    create_test_file(tmp_path, TEST_DATA['invalid_csv_content'], 'invalid.csv')
    create_test_file(tmp_path, TEST_DATA['empty_csv_content'], 'empty.csv')
    
    records, validation_summary = parse_all_files(str(tmp_path))
    
   
    assert len(records) == 3 
    assert validation_summary['files_processed'] == 3
    assert validation_summary['valid_files'] == 1
    assert validation_summary['invalid_files'] == 2


def test_parse_nonexistent_file():
    """Test parsing non-existent file"""
    records = parse_csv('/nonexistent/path/file.csv')
    assert records == []


def test_parse_unsupported_file_type(tmp_path):
    """Test parsing unsupported file type"""
    file_path = create_test_file(tmp_path, "some content", 'test.txt')
    
    records = parse_csv(str(file_path))
    assert records == [] 


def test_parse_empty_directory(tmp_path):
    """Test parsing empty directory"""
    records, validation_summary = parse_all_files(str(tmp_path))
    
    assert len(records) == 0
    assert validation_summary['files_processed'] == 0
    assert validation_summary['valid_files'] == 0
    assert validation_summary['invalid_files'] == 0


def test_parse_nonexistent_directory():
    """Test parsing non-existent directory"""
    records, validation_summary = parse_all_files('/nonexistent/directory')
    
    assert len(records) == 0
    assert 'error' in validation_summary
    assert validation_summary['error'] == 'Directory not found'