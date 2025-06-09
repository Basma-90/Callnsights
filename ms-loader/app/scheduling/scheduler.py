import time
import schedule
from app.db.database import save_to_postgres
from app.messaging.kafka_producer import publish_to_kafka
from app.config.logger import logger
from app.parsers import parse_all_files


def job():
    print("Running ETL job...")
    cdr_directory = "./cdr_files"

    valid_records, validation_summary = parse_all_files(cdr_directory)

    # Log validation summary
    logger.info(f"Validation Summary: {validation_summary}")
    
    if not valid_records:
        logger.warning("No valid records found to process")
        if validation_summary.get("files_with_errors"):
            logger.warning("Files with errors:")
            for file_error in validation_summary["files_with_errors"]:
                logger.warning(f"  {file_error['filename']}: {file_error['error']}")
        return

    logger.info(f"Processing {len(valid_records)} valid records")

    if save_to_postgres(valid_records):
        logger.info("Records saved to PostgreSQL")
        publish_to_kafka(valid_records)
        logger.info("Records published to Kafka")
    else:
        logger.error("Failed to save records to PostgreSQL")


def run():
    schedule.every(30).seconds.do(job)
    logger.info("Scheduler started - running every 30 seconds")
    while True:
        schedule.run_pending()
        time.sleep(1)