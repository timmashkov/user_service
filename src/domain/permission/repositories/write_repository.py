from typing import Any, Optional

from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from adapters.alchemy_adapter import AlchemyAdapter
from main.common.interfaces.repository_interfaces import AbstractWriteRepository
from main.database.models import Role


class RoleWriteRepository(AbstractWriteRepository):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        self._model = Role
        self._session: async_sessionmaker = session_adapter.transactional_session

    async def create_item(self, **kwargs: Any) -> Optional[Role]:
        async with self._session() as session:
            stmt = insert(self._model).values(kwargs).returning(self._model)
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()

    async def update_item(self, **kwargs: Any) -> Optional[Role]:
        async with self._session() as session:
            stmt = (
                update(self._model)
                .values(kwargs)
                .where(self._model.uuid == kwargs["uuid"])
                .returning(self._model)
            )
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()

    async def delete_item(self, **kwargs: Any) -> Optional[Role]:
        async with self._session() as session:
            stmt = (
                delete(self._model)
                .where(self._model.uuid == kwargs["uuid"])
                .returning(self._model)
            )
            answer = await session.execute(stmt)
            await session.commit()
        return answer.unique().scalar_one_or_none()
