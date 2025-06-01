import asyncio
import logging
from typing import Optional

from application.services.broker_service import BrokerMessageHandler
from domain.user.interfaces.read_repository_interface import UserReadRepositoryInterface
from infrastructure.common.base_entities.singleton import Singleton
from infrastructure.common.interfaces.broker_interface import AbstractBroker
from infrastructure.common.utils.safe_gather import safe_gather


class BrokerProcessManager(Singleton):
    def __init__(
        self,
        broker: AbstractBroker,
        user_read_repository: UserReadRepositoryInterface,
        queues: dict[str, str],
        logger: Optional[logging.Logger] = None,
    ) -> None:
        self.broker = broker
        self.queues = queues
        self._message_handler = BrokerMessageHandler(
            user_read_repository=user_read_repository, rabbit_adapter=broker
        )
        self._is_running = False
        self.logger = logger or logging
        self._consumer_task: Optional[asyncio.Task] = None

    async def initialize(self) -> None:
        """Инициализация подключения и очередей"""
        try:
            await self.broker.connect()
            await self._init_queues()
            self._is_running = True
            self.logger.info("Broker manager initialized successfully")
        except Exception as e:
            self.logger.error(f"Broker initialization failed: {e}")
            raise

    async def _init_queues(self) -> None:
        """Инициализация очередей"""
        await safe_gather(
            *[self.broker.init_queue(queue_name) for queue_name in self.queues.values()]
        )

        await self.broker.init_consumer(
            on_message=self._message_handler.check_user_exist_callback,
            routing_key=self.queues["user_check"],
        )

    async def start_consuming(self) -> None:
        """Запуск консуминга в фоновом режиме"""
        if not self._is_running:
            await self.initialize()

        self._consumer_task = asyncio.create_task(self._run_consuming())
        self.logger.info("Started consuming messages")

    async def _run_consuming(self) -> None:
        """Основной цикл обработки сообщений"""
        while self._is_running:
            try:
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                self.logger.info("Consuming stopped")
                break
            except Exception as e:
                self.logger.error(f"Error in consuming loop: {e}")
                await asyncio.sleep(1)

    async def stop_consuming(self) -> None:
        """Корректная остановка консуминга"""
        self._is_running = False
        if self._consumer_task:
            self._consumer_task.cancel()
            try:
                await self._consumer_task
            except asyncio.CancelledError:
                pass
        await self.broker.close()
        self.logger.info("Broker manager stopped")

    async def __aenter__(self):
        await self.start_consuming()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop_consuming()
