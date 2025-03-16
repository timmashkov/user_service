from typing import Any, Union
from uuid import UUID

from fastapi import Depends

from application.container import Container
from domain.user.entities.model import UserIncomingData
from main.common.base_entities.singleton import Singleton
from main.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
    AbstractWriteRepository,
)


class UserService(Singleton):
    def __init__(
        self,
        read_repository: AbstractReadRepository = Depends(Container.user_read_manager),
        write_repository: AbstractWriteRepository = Depends(
            Container.user_write_manager
        ),
    ) -> None:
        self.read_repository = read_repository
        self.write_repository = write_repository

    async def get_item(self, uuid: Union[str, UUID]):
        return await self.read_repository.get_item(uuid=uuid)

    async def get_items(self, filters: Any = None):
        return await self.read_repository.find(filters=filters)

    async def create_item(self, data: UserIncomingData):
        answer = data.model_dump()
        answer["password"] = answer["password"].get_secret_value()
        return await self.write_repository.create_item(**answer)

    async def update_item(self, uuid: Union[str, UUID], data: UserIncomingData):
        intel = data.model_dump()
        intel["uuid"] = uuid
        return await self.write_repository.update_item(**intel)

    async def delete_item(self, uuid: Union[str, UUID]):
        return await self.write_repository.delete_item(uuid=uuid)
