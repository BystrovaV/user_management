import json
import logging

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import UnroutableError

from core.exceptions import MessageDeliveryException
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
        self.channel.confirm_delivery()
        self.channel.exchange_declare(exchange="emails", exchange_type="fanout")
        message = {"email": email, "msg": msg}

        message_bytes = json.dumps(message).encode("utf-8")

        try:
            self.channel.basic_publish(
                exchange="emails", routing_key="", body=message_bytes, mandatory=True
            )
        except UnroutableError as e:
            logger.error(e)
            raise MessageDeliveryException
