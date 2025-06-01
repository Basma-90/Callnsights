import json
from datetime import datetime

from confluent_kafka import Producer

from app.config import KAFKA
from app.config.logger import logger


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def publish_to_kafka(records):
    """Publish records to Kafka with proper datetime handling"""
    if not records:
        return

    p = Producer({"bootstrap.servers": KAFKA["bootstrap_servers"]})
    logger.info(f"Connecting to Kafka at {KAFKA['bootstrap_servers']}")

    try:
        for record in records:
            json_data = json.dumps(record, cls=DateTimeEncoder)
            logger.debug(f"Publishing record to Kafka: {json_data}")
            p.produce(KAFKA["topic"], key=str(record["source"]), value=json_data)
            logger.info(f"Record published to Kafka topic {KAFKA['topic']}: {json_data}")
        p.flush()
        logger.info("Records published to Kafka successfully")
    except Exception as e:
        logger.error(f"Error publishing to Kafka: {str(e)}")
