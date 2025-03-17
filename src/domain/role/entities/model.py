from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from main.common.base_entities.patched_filter import PatchedFilter
from main.database.models import Role


class RoleIncomingData(BaseModel):
    name: str = Field(description=Role.name.comment)
    data: Optional[dict] = Field(description=Role.data.comment)


class RoleResultData(RoleIncomingData):
    uuid: UUID = Field(description=Role.uuid.comment)
    created_at: datetime = Field(description=Role.created_at.comment)
    updated_at: datetime = Field(description=Role.updated_at.comment)


class RoleFilter(PatchedFilter):
    uuid: Optional[UUID] = None
    name: Optional[str] = None

    class Constants(PatchedFilter.Constants):
        model = Role
