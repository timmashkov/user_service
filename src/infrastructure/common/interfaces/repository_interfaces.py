from abc import ABC, abstractmethod
from typing import Any, Union
from uuid import UUID

from sqlalchemy import select


class AbstractReadRepository(ABC):

    @classmethod
    def __set_filter(cls, query: select, filters: Any = None) -> select:
        pass

    @abstractmethod
    async def get_item(self, uuid: Union[str, UUID]) -> Any:
        pass

    @abstractmethod
    async def find(self, *args: Any, **kwargs: Any) -> Any:
        pass


class AbstractWriteRepository(ABC):

    @abstractmethod
    async def create_item(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def update_item(self, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    async def delete_item(self, uuid: Union[str, UUID]) -> Any:
        pass
