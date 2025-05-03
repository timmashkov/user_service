from fastapi import APIRouter, Depends

from domain.auth.entities.dto import LoginDTO, LoginResult, LogoutDTO
from domain.auth.entities.enums import AuthOptions
from domain.auth.entities.model import RefreshTokenModel
from presentation.interactor_fabric import AuthInteractorFactory


class AuthRouter:
    api_router = APIRouter(prefix="/auth", tags=["Auth"])
    auth_factory: AuthInteractorFactory = Depends()

    @staticmethod
    @api_router.post("/login", response_model=LoginResult)
    async def login(
        login_data: LoginDTO,
        auth_factory: AuthInteractorFactory = auth_factory,
    ) -> LoginResult:
        async with auth_factory.authenticate(option=AuthOptions.LOGIN) as authenticate:
            status = await authenticate(login_data)
        return status

    @staticmethod
    @api_router.post("/logout", response_model=LogoutDTO)
    async def logout(
        data: RefreshTokenModel,
        auth_factory: AuthInteractorFactory = auth_factory,
    ) -> LogoutDTO:
        async with auth_factory.authenticate(option=AuthOptions.LOGOUT) as authenticate:
            status = await authenticate(refresh_token=data.refresh_token)
        return status

    @staticmethod
    @api_router.post("/check", response_model=LoginResult)
    async def check_auth(
        data: RefreshTokenModel,
        auth_factory: AuthInteractorFactory = auth_factory,
    ) -> LoginResult:
        async with auth_factory.authenticate(
            option=AuthOptions.CHECK_AUTH
        ) as authenticate:
            status = await authenticate(refresh_token=data.refresh_token)
        return status

    @staticmethod
    @api_router.post("/refresh", response_model=LoginResult)
    async def refresh_tokens(
        data: RefreshTokenModel,
        auth_factory: AuthInteractorFactory = auth_factory,
    ) -> LoginResult:
        async with auth_factory.authenticate(
            option=AuthOptions.REFRESH_TOKEN
        ) as authenticate:
            status = await authenticate(refresh_token=data.refresh_token)
        return status
