import json
import pika
from typing import NamedTuple


class Message(NamedTuple):
    event_name: str
    event: dict


def init_event_creation(name: str, event: dict) -> None:
    message = Message(event_name=name, event=event)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1'))

    channel = connection.channel()

    channel.queue_declare(queue='message')

    channel.basic_publish(
        exchange='',
        routing_key='message',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )
