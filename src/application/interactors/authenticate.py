from adapters.auth.cookie_provider import CookieProvider
from adapters.auth.token_provider import TokenProvider
from application.services.user_service import UserService
from domain.auth.entities.dto import LoginDTO, LogoutDTO, TokenDTO
from domain.auth.exceptions.auth_exceptions import AuthenticationError
from infrastructure.common.base_entities.base_interactor import BaseInteractor


class Authenticate(BaseInteractor[LoginDTO, LogoutDTO]):
    def __init__(
        self,
        user_provider: UserService,
        token_provider: TokenProvider,
        cookie_provider: CookieProvider,
    ) -> None:
        self.user_provider = user_provider
        self.token_provider = token_provider
        self.cookie_provider = cookie_provider

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

        access_token = await self.token_provider.encode_token(user_id=user.uuid)

        self.cookie_provider.set_auth_cookie(access_token)

        return LogoutDTO(status=True)
