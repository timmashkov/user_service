from abc import ABC, abstractmethod
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from infrastructure.common.base_entities.patched_filter import PatchedFilter


class AbstractRouter(ABC):
    api_router: APIRouter
    filters: PatchedFilter
    service_client: Any
    input_model: BaseModel
    output_model: BaseModel

    @abstractmethod
    async def get_object(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def get_objects(self, filters: PatchedFilter, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def create_object(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def update_object(self, *args, **kwargs) -> Any:
        pass

    @abstractmethod
    async def delete_object(self, *args, **kwargs) -> Any:
        pass
