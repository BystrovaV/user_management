from fastapi import Depends
from pika.adapters.blocking_connection import BlockingChannel

from adapters.rabbitmq.publisher_service import RabbitMQ
from core.settings import Settings, get_settings


class RabbitMQDependency:
    def __init__(self):
        self.rabbit = None

    def __call__(self, settings: Settings = Depends(get_settings)):
        self.rabbit = RabbitMQ.start(settings) if not self.rabbit else self.rabbit

        return self.rabbit


get_rabbitmq_dependency = RabbitMQDependency()


def get_rabbitmq_channel(
    rabbitmq: RabbitMQ = Depends(get_rabbitmq_dependency),
) -> BlockingChannel:
    with rabbitmq.connection.channel() as channel:
        yield channel
