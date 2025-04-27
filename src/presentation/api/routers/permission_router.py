from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from pydantic import BaseModel

from application.services.permission_service import PermissionService
from domain.permission.entities.model import (
    PermissionFilter,
    PermissionIncomingData,
    PermissionResultData,
)
from main.common.interfaces.router_interface import AbstractRouter


class PermissionRouter(AbstractRouter):
    api_router = APIRouter(prefix="/permission", tags=["Permission"])
    filters: PermissionFilter = FilterDepends(PermissionFilter)
    service_client: PermissionService = Depends(PermissionService)
    input_model: BaseModel = PermissionIncomingData
    output_model: BaseModel = PermissionResultData

    @staticmethod
    @api_router.get("/{uuid}", response_model=output_model)
    async def get_object(
        uuid: Union[str, UUID],
        order_provider: PermissionService = service_client,
    ) -> output_model:
        return await order_provider.get_item(uuid=uuid)

    @staticmethod
    @api_router.get("/", response_model=List[output_model])
    async def get_objects(
        order_provider: PermissionService = service_client,
        filters: filters = filters,
    ) -> List[output_model]:
        return await order_provider.get_items(filters=filters)

    @staticmethod
    @api_router.post("/", response_model=output_model)
    async def create_object(
        data: input_model,
        order_provider: PermissionService = service_client,
    ) -> output_model:
        return await order_provider.create_item(data=data)

    @staticmethod
    @api_router.patch("/{uuid}", response_model=output_model)
    async def update_object(
        uuid: Union[str, UUID],
        data: input_model,
        order_provider: PermissionService = service_client,
    ) -> output_model:
        return await order_provider.update_item(uuid=uuid, data=data)

    @staticmethod
    @api_router.delete("/{uuid}", response_model=output_model)
    async def delete_object(
        uuid: Union[str, UUID],
        order_provider: PermissionService = service_client,
    ) -> output_model:
        return await order_provider.delete_item(uuid=uuid)
