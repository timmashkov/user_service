from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import Depends, Response

from adapters.auth.cookie_provider import CookieProvider
from adapters.auth.token_provider import TokenProvider
from application.container import Container
from application.interactors.authenticate import Authenticate
from application.services.user_service import UserService
from domain.auth.entities.enums import AuthOptions


class AuthInteractorFactory:
    def __init__(
        self,
        token_provider: TokenProvider = Depends(Container.token_manager),
        user_service: UserService = Depends(),
        response: Response = None,
    ):
        self.token_provider = token_provider
        self.user_service = user_service
        self.response = response

    @asynccontextmanager
    async def authenticate(
        self, option: AuthOptions
    ) -> AsyncContextManager[Authenticate]:
        cookie_adapter = CookieProvider(self.response) if self.response else None
        yield Authenticate(
            token_provider=self.token_provider,
            user_provider=self.user_service,
            cookie_provider=cookie_adapter,
            option=option,
        )
