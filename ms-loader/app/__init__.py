"""
CDR Loader Service
A microservice for loading and processing Call Detail Records (CDR)
"""

__version__ = "1.0.0"
__author__ = "Basma Sabry"

from app.scheduling.scheduler import run, job
from app.parsers import parse_all_files
from app.db.database import save_to_postgres
from app.messaging.kafka_producer import publish_to_kafka
from app.config import logger, POSTGRES, KAFKA
from app.validation.file_validator import validate_file, validate_record
from app.parsers import parse_csv, parse_json, parse_xml, parse_yaml

__all__ = [
    "run",
    "job",
    "parse_all_files",
    "save_to_postgres",
    "publish_to_kafka",
    "logger",
    "POSTGRES",
    "KAFKA",
    "validate_file",
    "validate_record",
    "parse_csv",
    "parse_json",
    "parse_xml",
    "parse_yaml"
]