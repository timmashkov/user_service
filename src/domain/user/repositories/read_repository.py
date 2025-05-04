from typing import Optional

from adapters.database.alchemy_adapter import AlchemyAdapter
from domain.user.interfaces.read_repository_interface import UserReadRepositoryInterface
from infrastructure.database.models import User
from infrastructure.database.repositories.read_repository import ReadRepository


class UserReadRepository(ReadRepository, UserReadRepositoryInterface):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        super().__init__(session_adapter, User)

    async def find_user(self, login: str) -> Optional[User]:
        async with self._session() as session:
            stmt = self.__get_query().where(self._model.login == login)
            answer = await session.execute(stmt)
        return answer.unique().scalar_one_or_none()
