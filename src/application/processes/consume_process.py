import asyncio
from multiprocessing import Process

from application.config import settings
from application.container import Container
from main.common.interfaces.broker_interface import AbstractBroker


async def _amqp_handler(
    rabbit_client: AbstractBroker = Container.rabbit_manager(),
) -> None:
    await rabbit_client.connect()
    await rabbit_client.init_queue(
        routing_key=settings.RABBIT_ROUTING_KEYS.test_routing_key
    )


def amqp_handler():
    asyncio.run(_amqp_handler())


amqp_process = Process(target=amqp_handler)
