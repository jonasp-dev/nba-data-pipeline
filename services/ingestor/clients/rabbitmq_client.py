import pika
import time
import logging
from config.config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD

def create_rabbitmq_connection():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = None
    for attempt in range(10):
        logging.info(f"Attempting to connect to RabbitMQ (attempt {attempt+1}/10)...")
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
            )
            channel = connection.channel()
            return channel
        except pika.exceptions.AMQPConnectionError:
            logging.warning(f"Connection failed (attempt {attempt+1}/10). Retrying...")
            time.sleep(3)
    else:
        logging.error("Could not connect to RabbitMQ after 10 tries.")
        exit(1)