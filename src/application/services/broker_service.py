from uuid import UUID

from aio_pika import IncomingMessage
from orjson import orjson

from application.config import settings
from domain.user.interfaces.read_repository_interface import UserReadRepositoryInterface
from infrastructure.common.base_entities.singleton import Singleton
from infrastructure.common.exceptions.broker_exceptions import SendingDataError
from infrastructure.common.interfaces.broker_interface import AbstractBroker
from infrastructure.database.models import Base


class BrokerMessageHandler(Singleton):
    def __init__(
        self,
        user_read_repository: UserReadRepositoryInterface,
        rabbit_adapter: AbstractBroker,
    ) -> None:
        self.user_read_repository = user_read_repository
        self.rabbit_adapter = rabbit_adapter

    @staticmethod
    def __message_body_getter(raw_message: IncomingMessage) -> dict:
        return orjson.loads(raw_message.body)

    @staticmethod
    def __table_to_dict(table: Base) -> dict:
        processed_data = table.as_dict()
        for key, value in processed_data.items():
            if isinstance(value, UUID):
                processed_data[key] = str(value)
        return processed_data

    async def check_user_exist_callback(self, message: IncomingMessage) -> None:
        try:
            user_uuid = self.__message_body_getter(raw_message=message).get("user_uuid")
            existing_user = await self.user_read_repository.get_item(uuid=user_uuid)
            await message.ack()
            if existing_user:
                await self.rabbit_adapter.send(
                    message=self.__table_to_dict(existing_user),
                    routing_key=settings.RABBIT_ROUTING_KEYS.user_check,
                )
        except Exception:
            raise SendingDataError
