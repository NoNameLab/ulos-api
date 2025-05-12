import json
import pika
from datetime import datetime
from fastapi import HTTPException

def publish_to_rabbitmq(
    task_id: int,
    user_id: int,
    remote_storage_path: str,
    task_definition: dict
):
    rabbitmq_host = "localhost"
    exchange_name = "processing-exchange"
    routing_key = "processing"

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type='direct', durable=True)

        message = {
            "taskId": str(task_id),
            "taskOwnerId": str(user_id),
            "filePath": remote_storage_path,
            "taskDefinition": task_definition
        }

        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(message)
        )
        connection.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RabbitMQ error: {str(e)}")
