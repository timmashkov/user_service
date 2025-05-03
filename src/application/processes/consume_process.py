import asyncio
from multiprocessing import Process
from typing import Callable

from infrastructure.common.base_entities.singleton import Singleton
from infrastructure.common.interfaces.broker_interface import AbstractBroker
from infrastructure.common.utils.safe_gather import safe_gather


class BrokerProcessManager(Singleton):
    def __init__(
        self,
        broker: AbstractBroker,
        queues: list[str],
    ) -> None:
        self.broker = broker
        self.queues = queues
        self.__broker_process = Process(target=self.start_broker)

    async def _init_broker_queues(self) -> None:
        await safe_gather(
            *[self.broker.init_queue(queue) for queue in self.queues],
            parallelism_size=len(self.queues),
        )

    async def _init_broker_issues(self) -> None:
        await self.broker.connect()
        await self._init_broker_queues()

    def start_broker(self) -> None:
        asyncio.run(self._init_broker_issues())

    def start_broker_process(self) -> Callable:
        return self.__broker_process.start

    def stop_broker_process(self) -> Callable:
        return self.__broker_process.close
