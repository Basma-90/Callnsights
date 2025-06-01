import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "db": os.getenv("POSTGRES_DB", "postgres"),
}

KAFKA = {
    "bootstrap_servers": os.getenv("KAFKA_SERVERS", "localhost:29092"),
    "topic": os.getenv("KAFKA_TOPIC", "cdr-records"),
    "group_id": os.getenv("KAFKA_GROUP_ID", "cdr-consumer-group"),
    "ssl": os.getenv("KAFKA_SSL", "false").lower() == "true",
}
