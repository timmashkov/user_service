from abc import abstractmethod
from typing import Any

from infrastructure.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
)


class UserReadRepositoryInterface(AbstractReadRepository):

    @abstractmethod
    async def find_user(self, login: str) -> Any:
        pass
