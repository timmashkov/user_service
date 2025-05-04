from adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.database.models import Role
from infrastructure.database.repositories.read_repository import ReadRepository


class RoleReadRepository(ReadRepository):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        super().__init__(session_adapter, Role)
