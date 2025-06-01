from contextlib import asynccontextmanager
from typing import AsyncContextManager

from fastapi import Depends, Response

from adapters.auth.cookie_adapter import CookieAdapter
from adapters.auth.token_adapter import TokenAdapter
from application.container import Container
from application.interactors.authenticate import Authenticate
from application.services.user_service import UserService
from domain.auth.entities.enums import AuthOptions


class InteractorFactory:
    def __init__(
        self,
        token_adapter: TokenAdapter = Depends(Container.token_manager),
        user_service: UserService = Depends(),
        response: Response = None,
    ) -> None:
        self.token_adapter = token_adapter
        self.user_service = user_service
        self.response = response

    @asynccontextmanager
    async def authenticate(
        self, option: AuthOptions
    ) -> AsyncContextManager[Authenticate]:
        cookie_adapter = CookieAdapter(self.response) if self.response else None
        yield Authenticate(
            token_adapter=self.token_adapter,
            user_provider=self.user_service,
            cookie_adapter=cookie_adapter,
            option=option,
        )
