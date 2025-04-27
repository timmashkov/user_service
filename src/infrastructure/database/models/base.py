import uuid
from datetime import datetime

from sqlalchemy import UUID, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        table_name = cls.__name__
        result = table_name[0] + "".join(
            map(lambda x: "_" + x if x.istitle() else x, table_name[1:])
        )
        return f"{result.lower()}s"

    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
        comment="Уникальный айди записи",
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now(), comment="Дата создания"
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now(),
        onupdate=datetime.now(),
        comment="Дата обновления",
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
