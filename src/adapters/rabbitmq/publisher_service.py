import json
import logging

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel

from core.exceptions import RabbitMQConnectionException
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
    def __init__(self, channel: BlockingChannel, settings: Settings):
        self.channel = channel
        self.settings = settings

    def publish_message(self, email: str, msg: str, subject: str):
        message = {"to_address": email, "message": msg, "subject": subject}

        # args = {
        #     'x-dead-letter-exchange': 'dlq_exchange',
        #     'x-dead-letter-routing-key': 'dlq'
        # }

        try:
            # self.channel.queue_declare(queue=self.settings.RABBIT_EMAIL_QUEUE, arguments=args)
            message_bytes = json.dumps(message).encode("utf-8")

            self.channel.basic_publish(
                exchange="",
                routing_key=self.settings.RABBIT_EMAIL_QUEUE,
                body=message_bytes,
            )
        except Exception as e:
            logger.info(e)
            raise RabbitMQConnectionException
