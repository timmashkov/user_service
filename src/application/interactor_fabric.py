from contextlib import contextmanager

from fastapi import Depends

from adapters.auth.token_provider import TokenProvider
from application.container import Container
from application.interactors.authenticate import Authenticate
from application.services.user_service import UserService


class AuthInteractorFactory:
    def __init__(
        self,
        token_provider: TokenProvider = Depends(Container.token_manager),
        user_service: UserService = Depends(),
    ):
        self.token_provider = token_provider
        self.user_service = user_service

    @contextmanager
    def authenticate(self) -> Authenticate:
        yield Authenticate(
            token_provider=self.token_provider,
            user_provider=self.user_service,
        )
