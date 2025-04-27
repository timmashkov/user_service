from adapters.auth.token_provider import TokenProvider
from application.services.user_service import UserService
from domain.auth.entities.dto import LoginDTO, LogoutDTO, TokenDTO
from domain.auth.exceptions.auth_exceptions import AuthenticationError
from main.common.base_entities.base_interactor import BaseInteractor


class Authenticate(BaseInteractor[LoginDTO, LogoutDTO]):
    def __init__(
        self,
        user_provider: UserService,
        token_provider: TokenProvider,
    ) -> None:
        self.user_provider = user_provider
        self.token_provider = token_provider

    async def __call__(self, incoming_data: LoginDTO) -> LogoutDTO:

        user = await self.user_provider.find_user(login=incoming_data.login)

        if not user:
            raise AuthenticationError

        token_data = TokenDTO(
            password=incoming_data.password,
            salt=user.login,
            encoded_pass=user.password,
        )

        if not await self.token_provider.verify_password(token_data):
            raise AuthenticationError

        return LogoutDTO(status=True)
