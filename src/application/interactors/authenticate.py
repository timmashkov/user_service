import logging
from typing import Optional, Union

from adapters.auth.cookie_adapter import CookieAdapter
from adapters.auth.token_adapter import TokenAdapter
from application.services.user_service import UserService
from domain.auth.entities.dto import LoginDTO, LoginResult, LogoutDTO, TokenDTO
from domain.auth.entities.enums import AuthOptions
from domain.auth.exceptions.auth_exceptions import AuthenticationError
from domain.auth.exceptions.token_exceptions import Unauthorized
from infrastructure.common.base_entities.base_interactor import BaseInteractor
from infrastructure.common.utils.safe_gather import safe_gather


class Authenticate(BaseInteractor[LoginDTO, LogoutDTO]):
    def __init__(
        self,
        user_provider: UserService,
        token_adapter: TokenAdapter,
        cookie_adapter: CookieAdapter,
        option: AuthOptions,
    ) -> None:
        self.user_provider = user_provider
        self.token_adapter = token_adapter
        self.cookie_adapter = cookie_adapter
        self.option = option

    async def __call__(
        self,
        incoming_data: Optional[LoginDTO] = None,
        refresh_token: Optional[str] = None,
    ) -> Union[LogoutDTO, LoginResult]:
        if self.option == AuthOptions.LOGIN:
            return await self._login(incoming_data)
        elif self.option == AuthOptions.LOGOUT:
            return await self._logout(refresh_token=refresh_token)
        elif self.option == AuthOptions.CHECK_AUTH:
            return await self._check_auth(refresh_token=refresh_token)
        elif self.option == AuthOptions.REFRESH_TOKEN:
            return await self._refresh_tokens(refresh_token=refresh_token)

    async def _login(self, incoming_data: LoginDTO) -> LoginResult:

        user = await self.user_provider.find_user(login=incoming_data.login)

        if not user:
            raise AuthenticationError

        token_data = TokenDTO(
            password=incoming_data.password,
            salt=user.login,
            encoded_pass=user.password,
        )

        if not await self.token_adapter.verify_password(token_data):
            raise AuthenticationError

        access_token, refresh_token = await safe_gather(
            *[
                self.token_adapter.encode_token(user_id=user.login),
                self.token_adapter.encode_refresh_token(user_id=user.login),
            ]
        )
        self.cookie_adapter.set_auth_cookie(access_token, key="access_token")
        self.cookie_adapter.set_auth_cookie(refresh_token, key="refresh_token")
        await self.token_adapter.save_tokens_to_session(
            access_token, refresh_token, user.login
        )
        return LoginResult(access_token=access_token, refresh_token=refresh_token)

    async def _logout(self, refresh_token: str) -> LogoutDTO:
        user_login = await self.token_adapter.decode_refresh_token(token=refresh_token)
        tokens = await self.token_adapter.get_tokens_from_session(user_login=user_login)

        if not tokens:
            raise Unauthorized

        try:
            await self.token_adapter.del_tokes_from_session(user_login)
            self.cookie_adapter.delete_auth_cookie()

            return LogoutDTO(status=True)

        except Exception as e:
            logging.error(f"Error while logging out: {e}")
            return LogoutDTO(status=False)

    async def _check_auth(self, refresh_token: str) -> LoginResult:
        user_login = await self.token_adapter.decode_refresh_token(token=refresh_token)

        if tokens := await self.token_adapter.get_tokens_from_session(
            user_login=user_login
        ):
            return LoginResult(**tokens)
        raise Unauthorized

    async def _refresh_tokens(self, refresh_token: str) -> LoginResult:
        user_login = await self.token_adapter.decode_refresh_token(token=refresh_token)
        tokens = await self.token_adapter.get_tokens_from_session(user_login=user_login)

        if tokens:
            new_tokens = await self.token_adapter.refresh_tokens(
                tokens.get("refresh_token")
            )
            await self.token_adapter.refresh_tokens_in_session(user_login, tokens)
            self.cookie_adapter.refresh_auth_cookie(new_tokens)
            return LoginResult(**new_tokens)
        raise Unauthorized
