from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from main.common.base_entities.patched_filter import PatchedFilter
from main.database.models import Permission


class PermissionIncomingData(BaseModel):
    name: str = Field(description=Permission.name.comment)
    layer: str = Field(description=Permission.layer.comment)
    data: Optional[dict] = Field(description=Permission.data.comment)


class PermissionResultData(PermissionIncomingData):
    uuid: UUID = Field(description=Permission.uuid.comment)
    created_at: datetime = Field(description=Permission.created_at.comment)
    updated_at: datetime = Field(description=Permission.updated_at.comment)


class PermissionFilter(PatchedFilter):
    uuid: Optional[UUID] = None
    name: Optional[str] = None
    layer: Optional[str] = None

    class Constants(PatchedFilter.Constants):
        model = Permission
