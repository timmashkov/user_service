from typing import Any, Optional, Union
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.common.interfaces.repository_interfaces import (
    AbstractReadRepository,
)
from infrastructure.database.models import User


class UserReadRepository(AbstractReadRepository):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        self._model = User
        self._session: async_sessionmaker = session_adapter.autocommit_session

    @classmethod
    def __set_filter(cls, query: select, filters: Any = None) -> select:
        if filters:
            query = filters.filter(query)
        return query

    def __get_query(self) -> select:
        query = select(self._model)
        return query

    async def get_item(self, uuid: Union[str, UUID]) -> Optional[User]:
        async with self._session() as session:
            stmt = self.__get_query().where(self._model.uuid == uuid)
            answer = await session.execute(stmt)
        return answer.unique().scalar_one_or_none()

    async def find_user(self, login: str) -> Optional[User]:
        async with self._session() as session:
            stmt = self.__get_query().where(self._model.login == login)
            answer = await session.execute(stmt)
        return answer.unique().scalar_one_or_none()

    async def find(
        self,
        filters: Any = None,
    ) -> Union[list, select]:
        query = self.__get_query()
        query = self.__set_filter(query, filters)
        async with self._session() as session:
            result = await session.execute(query)
            return result.scalars().unique().all()
