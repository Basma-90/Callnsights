import os

from .csv_parser import parse_csv
from .json_parser import parse_json
from .xml_parser import parse_xml
from .yaml_parser import parse_yaml


def parse_all_files(directory):
    records = []

    parsers = {
        ".csv": parse_csv,
        ".json": parse_json,
        ".xml": parse_xml,
        ".yaml": parse_yaml,
    }

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        file_ext = os.path.splitext(filename)[1].lower()

        if file_ext in parsers:
            try:
                file_records = parsers[file_ext](filepath)
                if file_records:
                    print(f"Parsing {filename}...")
                    records.extend(file_records)
            except Exception as e:
                print(f"Error parsing {filename}: {str(e)}")

    return records
