from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class UserCreateDTO:
    first_name: str
    last_name: str
    patronymic: str
    login: str
    password: str
    email: str
    age: int
    phone_number: str
    data: dict
    is_verified: bool
    is_superuser: bool
    is_active: bool


@dataclass(frozen=True)
class UserResultDTO(UserCreateDTO):
    uuid: UUID
    created_at: datetime
    updated_at: datetime
