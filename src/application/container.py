from adapters.alchemy_adapter import AlchemyAdapter
from adapters.rabbit_adapter import RabbitMQAdapter
from application.config import settings
from domain.role.repositories.read_repository import (
    PermissionReadRepository,
    RoleReadRepository,
)
from domain.role.repositories.write_repository import (
    PermissionWriteRepository,
    RoleWriteRepository,
)
from domain.user.repositories.read_repository import UserReadRepository
from domain.user.repositories.write_repository import UserWriteRepository
from main.common.base_entities.singleton import OnlyContainer, Singleton


class Container(Singleton):

    alchemy_manager = OnlyContainer(
        AlchemyAdapter,
        dialect=settings.POSTGRES.dialect,
        host=settings.POSTGRES.host,
        login=settings.POSTGRES.login,
        password=settings.POSTGRES.password,
        port=settings.POSTGRES.port,
        database=settings.POSTGRES.database,
        echo=settings.POSTGRES.echo,
    )

    rabbit_manager = OnlyContainer(
        RabbitMQAdapter,
        **settings.RABBIT_MQ,
    )

    user_read_manager = OnlyContainer(
        UserReadRepository,
        session_adapter=alchemy_manager(),
    )

    user_write_manager = OnlyContainer(
        UserWriteRepository,
        session_adapter=alchemy_manager(),
    )

    role_read_manager = OnlyContainer(
        RoleReadRepository,
        session_adapter=alchemy_manager(),
    )

    role_write_manager = OnlyContainer(
        RoleWriteRepository,
        session_adapter=alchemy_manager(),
    )

    permission_read_manager = OnlyContainer(
        PermissionReadRepository,
        session_adapter=alchemy_manager(),
    )

    permission_write_manager = OnlyContainer(
        PermissionWriteRepository,
        session_adapter=alchemy_manager(),
    )
