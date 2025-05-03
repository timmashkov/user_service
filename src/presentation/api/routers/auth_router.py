from fastapi import APIRouter, Depends

from domain.auth.entities.dto import LoginDTO
from domain.auth.entities.enums import AuthOptions
from presentation.interactor_fabric import AuthInteractorFactory


class AuthRouter:
    api_router = APIRouter(prefix="/auth", tags=["Auth"])
    # filters: UserFilter = FilterDepends(UserFilter)
    # service_client: UserService = Depends(UserService)
    # input_model: BaseModel = UserIncomingData
    # output_model: BaseModel = UserResultData

    @staticmethod
    @api_router.post("/login")
    async def login(
        login_data: LoginDTO,
        auth_factory: AuthInteractorFactory = Depends(),
    ):
        async with auth_factory.authenticate(option=AuthOptions.LOGIN) as authenticate:
            status = await authenticate(login_data)
        return status

    @staticmethod
    @api_router.post("/logout")
    async def logout(
        refresh_token: str,
        auth_factory: AuthInteractorFactory = Depends(),
    ):
        async with auth_factory.authenticate(option=AuthOptions.LOGOUT) as authenticate:
            status = await authenticate(refresh_token=refresh_token)
        return status

    @staticmethod
    @api_router.post("/check")
    async def check_auth(
        refresh_token: str,
        auth_factory: AuthInteractorFactory = Depends(),
    ):
        async with auth_factory.authenticate(
            option=AuthOptions.CHECK_AUTH
        ) as authenticate:
            status = await authenticate(refresh_token=refresh_token)
        return status

    @staticmethod
    @api_router.post("/refresh")
    async def refresh_tokens(
        refresh_token: str,
        auth_factory: AuthInteractorFactory = Depends(),
    ):
        async with auth_factory.authenticate(
            option=AuthOptions.REFRESH_TOKEN
        ) as authenticate:
            status = await authenticate(refresh_token=refresh_token)
        return status
