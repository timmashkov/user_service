import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncContextManager, Optional

from fastapi import APIRouter, FastAPI

from infrastructure.common.base_entities.singleton import Singleton


class ApiServer(Singleton):
    def __init__(
        self,
        name: str,
        routers: list[APIRouter] = None,
        start_callbacks: list[callable] = None,
        stop_callbacks: list[callable] = None,
        logging_config: Optional[dict] = logging.getLogger(),
    ) -> None:
        self.name = name
        self.logging_config = logging_config
        self.app = FastAPI(
            title=name,
            lifespan=self._lifespan,
        )
        self.routers = routers or []
        self._init_routers()
        self.start_callbacks = start_callbacks or []
        self.stop_callbacks = stop_callbacks or []

    def _init_routers(self) -> None:
        for router in self.routers:
            self.app.include_router(router)
        logging.info("Инициализация routers прошла успешно")

    @asynccontextmanager
    async def _lifespan(self, _app: FastAPI) -> AsyncContextManager:
        for callback in self.start_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        logging.info("Инициализация startup callbacks прошла успешно")

        yield

        for callback in self.stop_callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback()
            else:
                await asyncio.to_thread(callback)
        logging.info("Инициализация shutdown callbacks прошла успешно")
