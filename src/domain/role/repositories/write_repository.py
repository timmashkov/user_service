from adapters.database.alchemy_adapter import AlchemyAdapter
from infrastructure.database.models import Role
from infrastructure.database.repositories.write_repository import WriteRepository


class RoleWriteRepository(WriteRepository):

    def __init__(self, session_adapter: AlchemyAdapter) -> None:
        super().__init__(session_adapter, Role)
