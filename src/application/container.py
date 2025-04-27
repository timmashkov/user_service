from redis.asyncio import Redis

from adapters.auth.token_provider import TokenProvider
from adapters.broker.rabbit_adapter import RabbitMQAdapter
from adapters.database.alchemy_adapter import AlchemyAdapter
from application.config import settings
from domain.permission.repositories.read_repository import PermissionReadRepository
from domain.permission.repositories.write_repository import PermissionWriteRepository
from domain.role.repositories.read_repository import RoleReadRepository
from domain.role.repositories.write_repository import RoleWriteRepository
from domain.user.repositories.read_repository import UserReadRepository
from domain.user.repositories.write_repository import UserWriteRepository
from main.common.base_entities.singleton import OnlyContainer, Singleton


class Container(Singleton):

    redis = OnlyContainer(
        Redis,
        **settings.REDIS,
        decode_responses=True,
    )

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
        queue_list=settings.RABBIT_ROUTING_KEYS,
    )

    token_manager = OnlyContainer(
        TokenProvider,
        secret=settings.AUTH.secret,
        exp=settings.AUTH.expiration,
        api_x_key_header=settings.AUTH.api_x_key_header,
        iterations=settings.AUTH.iterations,
        hash_name=settings.AUTH.hash_name,
        formats=settings.AUTH.formats,
        algorythm=settings.AUTH.algorythm,
        redis_client=redis(),
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
