import time
import schedule
from app.db.database import save_to_postgres
from app.messaging.kafka_producer import publish_to_kafka
from app.config.logger import logger
from app.parsers import parse_all_files


def job():
    print("Running ETL job...")
    cdr_directory = "./cdr_files"

    records = parse_all_files(cdr_directory)

    if not records:
        logger.warning("No records found to process")
        return

    if save_to_postgres(records):
        logger.info("Records saved to PostgreSQL")
        publish_to_kafka(records)
        logger.info("Records published to Kafka")
    else:
        logger.error("Failed to save records to PostgreSQL")


def run():
    schedule.every(30).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
