import asyncio
import logging
from typing import Any, Callable, List, Optional, Union

from aio_pika import Message, RobustConnection, connect_robust
from aio_pika.abc import AbstractChannel
from yarl import URL

from infrastructure.common.interfaces.broker_interface import AbstractBroker


class RabbitMQAdapter(AbstractBroker):

    def __init__(
        self,
        host: str,
        port: Union[int, str],
        login: str,
        password: str,
        protocol: str = "amqp",
        timeout: int = 10,
        queue_list: Optional[List[str]] = None,
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.connection: Optional[RobustConnection] = None
        self.queues: dict = {}
        self.queue_list: list = queue_list if queue_list else []
        self.channel: Optional[AbstractChannel] = None

        self.logger = logger or logging
        self.protocol = protocol
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.timeout = timeout

    @property
    def url(self) -> URL:
        return URL(
            f"{self.protocol}://{self.login}:{self.password}@{self.host}:{self.port}/"
        )

    async def connect(self, **kwargs: Any) -> None:
        self.connection = await connect_robust(url=self.url, **kwargs)
        if self.connection:
            self.channel = await self.connection.channel()
            self.logger.info("Successfully connected", self.url.with_password("******"))
        else:
            self.logger.error("Error while connecting")

    async def init_queue(self, routing_key: str, **kwargs: Any) -> None:
        if self.connection and self.channel:
            self.queues[routing_key] = await self.channel.declare_queue(
                name=routing_key, **kwargs
            )
            self.logger.info("Queue has been created %s", routing_key)
        else:
            raise ConnectionError("Error while creating queue")

    async def init_queues(self, **kwargs):
        if self.connection and self.channel:
            for routing_key in self.queue_list:
                await self.channel.declare_queue(name=routing_key, **kwargs)
            self.logger.info("Queues has been created")
        else:
            raise ConnectionError("Error while creating queues")

    async def close(self) -> None:
        if self.connection and not self.connection.is_closed:
            await self.connection.close()
        self.logger.info("Successfully disconnected", self.url.with_password("******"))

    async def init_consumer(
        self, routing_key: str, on_message: Callable, **kwargs: Any
    ) -> None:
        try:
            await self.queues[routing_key].consume(callback=on_message, **kwargs)
        except Exception as e:
            self.logger.error(f"Error while consuming: {e}")

    async def send(
        self, message: Union[str, bytes, dict, list], routing_key: str, **kwargs: Any
    ) -> None:
        processed_message = Message(
            body=self.serialize_message(message),
            headers=kwargs.get("headers", {}),
            delivery_mode=kwargs.get("delivery_mode"),
        )
        if self.channel:
            asyncio.create_task(
                self.channel.default_exchange.publish(
                    processed_message, routing_key=routing_key
                )
            )
            self.logger.info("Successfully sent to queue %s", routing_key)
        else:
            self.logger.error("Error while sending message")

    async def get_message(self, routing_key: str) -> Any:
        while True:
            message = await self.queues[routing_key].get(
                timeout=self.timeout, fail=False
            )
            if message:
                await message.ack()
                return message
            await asyncio.sleep(0.01)
