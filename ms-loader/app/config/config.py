import os
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def parse_postgres_port(port_str):
    """Extract port from either a number or connection string"""
    if port_str.startswith('tcp://'):
        parsed = urlparse(port_str)
        return int(parsed.port) if parsed.port else 5432
    return int(port_str)

POSTGRES = {
    "host": os.getenv("POSTGRES_HOST", "postgres.kafka.svc.cluster.local"),
    "port": parse_postgres_port(os.getenv("POSTGRES_PORT", "5432")),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "db": os.getenv("POSTGRES_DB", "postgres"),
}

KAFKA = {
    "bootstrap_servers": os.getenv("KAFKA_SERVERS", "ms-kafka-simple-kafka-bootstrap.kafka.svc.cluster.local:9092"),
    "topic": os.getenv("KAFKA_TOPIC", "cdr-records"),
    "group_id": os.getenv("KAFKA_GROUP_ID", "cdr-consumer-group"),
    "ssl": os.getenv("KAFKA_SSL", "false").lower() == "true",
}
