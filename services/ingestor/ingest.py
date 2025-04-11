import json
import logging
from clients.rabbitmq_client import create_rabbitmq_connection
from clients.s3_client import create_s3_client
from clients.db_client import create_db_connection
from config.config import S3_BUCKET

channel = create_rabbitmq_connection()
channel.queue_declare(queue="nba-json-tasks")

s3 = create_s3_client()

db_conn = create_db_connection()
cursor = db_conn.cursor()

def is_processed(key):
    cursor.execute("SELECT 1 FROM processed_files WHERE s3_key = %s", (key,))
    return cursor.fetchone() is not None

def mark_as_processed(key, bucket, etag):
    logging.info(f"Marking {key} as processed")
    cursor.execute(
        "INSERT INTO processed_files (s3_key, s3_bucket, s3_etag, status) VALUES (%s, %s, %s, %s)",
        (key, bucket, etag, 'queued')
    )
    db_conn.commit()

def ingest():
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=S3_BUCKET):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            etag = obj["ETag"].strip('"')  # Remove quotes
            message = {
                "s3_key": key,
                "s3_bucket": S3_BUCKET,
                "s3_etag": etag
            }
            if not is_processed(key):
                logging.info(f"File {key} not processed, ingesting...")
                channel.basic_publish(
                    exchange='',
                    routing_key='nba-json-tasks',
                    body=json.dumps(message)
                )
                mark_as_processed(key, S3_BUCKET, etag)
            else:
                logging.info(f"File {key} already processed, skipping.")

    db_conn.close()
    channel.connection.close()