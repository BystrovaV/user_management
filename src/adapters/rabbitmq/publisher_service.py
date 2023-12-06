import json
import logging

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel

from core.settings import Settings
from ports.repositories.notification_service import NotificationService

logger = logging.getLogger(__name__)


class RabbitMQ:
    def __init__(self, connection):
        self.connection = connection

    @classmethod
    def start(cls, settings: Settings):
        connection = BlockingConnection(
            ConnectionParameters(
                host=settings.RABBIT_HOST,
                port=settings.RABBIT_PORT,
                credentials=PlainCredentials(
                    settings.RABBIT_USER, settings.RABBIT_PASSWORD
                ),
            )
        )
        connection.channel()
        return cls(connection)

    def __del__(self):
        self.connection.close()


class RabbitMQService(NotificationService):
    def __init__(self, channel: BlockingChannel):
        self.channel = channel

    def publish_message(self, email: str, msg: str):
        message = {"email": email, "msg": msg}

        self.channel.queue_declare(queue="reset_password")

        message_bytes = json.dumps(message).encode("utf-8")

        self.channel.basic_publish(
            exchange="", routing_key="reset_password", body=message_bytes
        )
