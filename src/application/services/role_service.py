from typing import Any, Union
from uuid import UUID

from fastapi import Depends

from application.container import Container
from domain.role.entities.model import RoleIncomingData
from infrastructure.common.base_entities.singleton import Singleton
from infrastructure.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
    AbstractWriteRepository,
)


class RoleService(Singleton):
    def __init__(
        self,
        read_repository: AbstractReadRepository = Depends(Container.role_read_manager),
        write_repository: AbstractWriteRepository = Depends(
            Container.role_write_manager
        ),
    ) -> None:
        self.read_repository = read_repository
        self.write_repository = write_repository

    async def get_item(self, uuid: Union[str, UUID]):
        return await self.read_repository.get_item(uuid=uuid)

    async def get_items(self, filters: Any = None):
        return await self.read_repository.find(filters=filters)

    async def create_item(self, data: RoleIncomingData):
        return await self.write_repository.create_item(**data.model_dump())

    async def update_item(self, uuid: Union[str, UUID], data: RoleIncomingData):
        intel = data.model_dump()
        intel["uuid"] = uuid
        return await self.write_repository.update_item(**intel)

    async def delete_item(self, uuid: Union[str, UUID]):
        return await self.write_repository.delete_item(uuid=uuid)
