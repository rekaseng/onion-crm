import sys
import os

# Add 'src' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import json
import pika
from application.rabbitmq_consumer.order_consumer import order_consumer
from config import settings

def listen_message(queueName: str, on_message_callback):
    connParameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        virtual_host=settings.RABBITMQ_VIRTUAL_HOST,
        port=settings.RABBITMQ_PORT,
        heartbeat=30,
        connection_attempts=5,
        credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    )
    try:
        connection = pika.BlockingConnection(connParameters)
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queueName, on_message_callback=on_message_callback)
        channel.start_consuming()
    except Exception as e:
        print(f"Error in RabbitMQ connection or consuming: {e}")
    finally:
        if connection.is_open:
            connection.close()
