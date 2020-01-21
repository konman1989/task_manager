import json
import pika


def init_task_creation(task):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='127.0.0.1'))
    channel = connection.channel()

    channel.queue_declare(queue='task')

    channel.basic_publish(
        exchange='',
        routing_key='task',
        body=json.dumps(task),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )