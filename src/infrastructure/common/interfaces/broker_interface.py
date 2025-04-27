from abc import ABC, abstractmethod
from typing import Any, Callable, Union

from orjson import dumps, loads

from infrastructure.common.exceptions.serialize_exceptions import (
    DeserializationError,
    SerializationError,
)


class AbstractBroker(ABC):

    @staticmethod
    def serialize_message(message: Union[str, bytes, list, dict]) -> bytes:
        try:
            if isinstance(message, str):
                return message.encode("utf-8")
            if isinstance(message, (list, dict)):
                return dumps(message)
            return message
        except (ValueError, TypeError):
            raise SerializationError(data=message)

    @staticmethod
    def deserialize_message(message: bytes) -> Any:
        try:
            return loads(message)
        except (ValueError, TypeError):
            raise DeserializationError(data=message)

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def init_queue(self, routing_key: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    async def send(
        self, message: Union[str, bytes, list, dict], routing_key: str, **kwargs: Any
    ) -> None:
        pass

    @abstractmethod
    async def init_consumer(
        self, routing_key: str, on_message: Callable, **kwargs: Any
    ) -> None:
        pass

    @abstractmethod
    async def get_message(self, routing_key: str) -> Any:
        pass
