from fastapi import APIRouter, Depends

from domain.auth.entities.dto import LoginDTO
from presentation.interactor_fabric import AuthInteractorFactory


class AuthRouter:
    api_router = APIRouter(prefix="/auth", tags=["Auth"])
    # filters: UserFilter = FilterDepends(UserFilter)
    # service_client: UserService = Depends(UserService)
    # input_model: BaseModel = UserIncomingData
    # output_model: BaseModel = UserResultData

    @staticmethod
    @api_router.post("/")
    async def get_auth_test(
        login_data: LoginDTO,
        auth_factory: AuthInteractorFactory = Depends(),
    ):
        async with auth_factory.authenticate() as authenticate:
            status = await authenticate(login_data)
        return status
