import pika
import json
import os

def rabConnect():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(os.environ['RAB']))
        channel = connection.channel()
    except Exception as e:
        print(f"Failed to connect to rabbitMQ {e}")
    
    return channel

def rabPublishMessage(ch, message):
    try:
        ch.basic_publish(
            exchange="",
            routing_key="task-queue",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  
            )
        )
    except Exception as e:
        print(f"Failed publishing the message{e}")

