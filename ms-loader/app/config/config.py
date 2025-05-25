import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "user": os.getenv("POSTGRES_USER", "cdr_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "cdr_password"),
    "db": os.getenv("POSTGRES_DB", "cdr_db"),
}

KAFKA = {
    "bootstrap_servers": os.getenv("KAFKA_SERVERS", "localhost:9092"),
    "topic": os.getenv("KAFKA_TOPIC", "cdr-records"),
}
