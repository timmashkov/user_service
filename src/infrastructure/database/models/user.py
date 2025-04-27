from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

if TYPE_CHECKING:
    from infrastructure.database.models.role import Role


class User(Base):

    first_name: Mapped[str] = mapped_column(
        String,
        unique=False,
        nullable=False,
        comment="Имя пользователя",
    )
    last_name: Mapped[str] = mapped_column(
        String,
        unique=False,
        nullable=False,
        comment="Фамилия пользователя",
    )
    patronymic: Mapped[str] = mapped_column(
        String,
        unique=False,
        nullable=False,
        comment="Отчество пользователя",
    )
    login: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        comment="Логин пользователя",
    )
    password: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
        comment="Зашифрованный пароль пользователя",
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        comment="Email пользователя",
    )
    age: Mapped[int] = mapped_column(
        Integer,
        unique=False,
        nullable=False,
        comment="Возраст пользователя",
    )
    phone_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        comment="Телефонный номер пользователя",
    )
    data: Mapped[dict] = mapped_column(
        JSONB,
        server_default="{}",
        default={},
        comment="Дополнительные данные",
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Статус подтверждения",
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Статус супер-пользователя",
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        comment="Статус активности",
    )
    roles: Mapped[List["Role"]] = relationship(
        secondary="user_roles",
        back_populates="users",
        lazy="joined",
    )
