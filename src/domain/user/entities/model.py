from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, SecretStr

from main.common.base_entities.patched_filter import PatchedFilter
from main.database.models import User


class UserIncomingData(BaseModel):
    first_name: str = Field(description=User.first_name.comment)
    last_name: str = Field(description=User.last_name.comment)
    patronymic: str = Field(description=User.patronymic.comment)
    login: str = Field(description=User.login.comment)
    password: SecretStr = Field(description=User.password.comment)
    email: EmailStr = Field(description=User.email.comment)
    age: int = Field(description=User.age.comment)
    phone_number: str = Field(description=User.phone_number.comment)
    data: Optional[dict] = Field(description=User.data.comment)
    is_verified: bool = Field(description=User.is_verified.comment)
    is_superuser: bool = Field(description=User.is_superuser.comment)
    is_active: bool = Field(description=User.is_active.comment)


class UserResultData(UserIncomingData):
    uuid: UUID = Field(description=User.uuid.comment)
    created_at: datetime = Field(description=User.created_at.comment)
    updated_at: datetime = Field(description=User.updated_at.comment)


class UserFilter(PatchedFilter):
    uuid: Optional[UUID] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    patronymic: Optional[str] = None
    email: Optional[EmailStr] = None
    is_verified: Optional[bool] = False
    is_superuser: Optional[bool] = False
    is_active: Optional[bool] = True

    class Constants(PatchedFilter.Constants):
        model = User
