"""
CDR Loader Service
A microservice for loading and processing Call Detail Records (CDR)
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from app.scheduling.scheduler import run, job
from app.parsers import parse_all_files
from app.db.database import save_to_postgres
from app.messaging.kafka_producer import publish_to_kafka
from app.config import logger, POSTGRES, KAFKA

__all__ = [
    "run",
    "job",
    "parse_all_files",
    "save_to_postgres",
    "publish_to_kafka",
    "logger",
    "POSTGRES",
    "KAFKA"
]