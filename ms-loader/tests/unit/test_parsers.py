import os
from app.parsers import parse_all_files, parse_csv, parse_json, parse_xml

from tests.unit import TEST_DATA, TEST_RECORD, create_test_file

def test_parse_csv(tmp_path):
    file_path = create_test_file(tmp_path, TEST_DATA['csv_content'], 'test.csv')
    
    records = parse_csv(str(file_path))
    assert len(records) == 1
    assert records[0]['source'] == TEST_RECORD['source']

def test_parse_json(tmp_path):
    file_path = create_test_file(tmp_path, TEST_DATA['json_content'], 'test.json')

    records = parse_json(str(file_path))
    assert len(records) == 1
    assert records[0]['source'] == TEST_RECORD['source']

def test_parse_xml(tmp_path):
    file_path = create_test_file(tmp_path, TEST_DATA['xml_content'], 'test.xml')
    
    records = parse_xml(str(file_path))
    assert len(records) == 1
    assert records[0]['source'] == TEST_RECORD['source']

def test_parse_all_files(tmp_path):
    create_test_file(tmp_path, TEST_DATA['csv_content'], 'test.csv')
    create_test_file(tmp_path, TEST_DATA['json_content'], 'test.json')
    create_test_file(tmp_path, TEST_DATA['xml_content'], 'test.xml')
    
    records = parse_all_files(str(tmp_path))
    assert len(records) == 3
    assert all(record['source'] == TEST_RECORD['source'] for record in records)

