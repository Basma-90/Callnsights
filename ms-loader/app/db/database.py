import psycopg2
from app.config import POSTGRES
from app.config.logger import logger


def connect():
    try:
        logger.debug("Connecting to PostgreSQL database")
        return psycopg2.connect(
            host=POSTGRES["host"],
            port=POSTGRES["port"],
            dbname=POSTGRES["db"],
            user=POSTGRES["user"],
            password=POSTGRES["password"],
        )
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL database: {e}")
        return None


def is_file_processed(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT EXISTS(SELECT 1 FROM processed_files WHERE filename = %s)",
            (filename,),
        )
        return cur.fetchone()[0]
    finally:
        cur.close()
        conn.close()


def mark_file_as_processed(filename):
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO processed_files (filename) VALUES (%s)", (filename,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def save_to_postgres(records):
    if not records:
        logger.warning("No records to save to PostgreSQL")
        return False
    conn = connect()
    if conn is None:
        logger.error("Failed to connect to PostgreSQL database")
        return False
    files_records = {}
    for record in records:
        if "file_name" not in record:
            logger.warning(f"Record missing file_name: {record}")
            continue
        file_name = record["file_name"]
        if file_name not in files_records:
            files_records[file_name] = []
        files_records[file_name].append(record)

    success = False
    conn = connect()
    cur = conn.cursor()
    try:
        for file_name, file_records in files_records.items():
            if is_file_processed(file_name):
                logger.info(f"File {file_name} has already been processed. Skipping.")
                continue

            for record in file_records:
                cur.execute(
                    """
                    INSERT INTO cdrs (source, destination, starttime, service, usage, file_name)
                    VALUES (%s, %s, %s, %s, %s ,%s)
                """,
                    (
                        record["source"],
                        record["destination"],
                        record["starttime"],
                        record["service"],
                        float(record["usage"]),
                        record["file_name"]
                        if "file_name" in record else None,
                    ),
                )

            mark_file_as_processed(file_name)
            logger.info(f"Processed {len(file_records)} records from file {file_name}")
            success = True

        conn.commit()
        return success

    except Exception as e:
        conn.rollback()
        logger.error(f"Error saving records to PostgreSQL: {str(e)}")
        logger.exception("Exception occurred while saving records to PostgreSQL")
        return False
    finally:
        cur.close()
        conn.close()
