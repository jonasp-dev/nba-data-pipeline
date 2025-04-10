import boto3
import json
import os
import pika
import time
import psycopg2
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "your-s3-bucket-name")
RABBITMQ_HOST = os.getenv("RABBITMQ_URL", "your-rabbitmq-url")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", 5672)
ACCESS_ID = os.getenv("AWS_ACCESS_KEY_ID", "your-access-key-id")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "your-access-key")

log_dir = Path("/app/logs/ingestor")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=log_dir / 'ingestor.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)
logging.info("Starting the ingestor service")
s3 = boto3.client("s3", region_name=AWS_REGION, aws_access_key_id=ACCESS_ID,
         aws_secret_access_key= AWS_SECRET_ACCESS_KEY)

connection = None
credentials = pika.PlainCredentials('user', 'password')
for attempt in range(10):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )
        channel = connection.channel()
        break
    except pika.exceptions.AMQPConnectionError:
        print(f"Connection failed (attempt {attempt+1}/10). Retrying...")
        time.sleep(3)
else:
    print("Could not connect to RabbitMQ after 10 tries.")
    exit(1)

channel = connection.channel()
channel.queue_declare(queue="nba-json-tasks")

db_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "postgres"),
    database=os.getenv("POSTGRES_DB", "nba_data"),
    user=os.getenv("POSTGRES_USER", "user"),
    password=os.getenv("POSTGRES_PASSWORD", "password")
)

cursor = db_conn.cursor()

def is_processed(key):
    cursor.execute("SELECT 1 FROM processed_files WHERE s3_key = %s", (key,))
    return cursor.fetchone() is not None

def mark_as_processed(key, bucket, etag):
    print(f"Marking {key} as processed")
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
                print(f"Ingesting new file: {key}")
                channel.basic_publish(
                    exchange='',
                    routing_key='nba-json-tasks',
                    body=json.dumps(message)
                )
                mark_as_processed(key, S3_BUCKET, etag)
            else:
                print(f"File {key} already processed, skipping.")
                logging.info(f"File {key} already processed, skipping.")
ingest()
connection.close()