from typing import List, Union
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from pydantic import BaseModel

from application.interactor_fabric import AuthInteractorFactory
from application.services.user_service import UserService
from domain.auth.entities.dto import LoginDTO
from domain.user.entities.model import UserFilter, UserIncomingData, UserResultData
from main.common.interfaces.router_interface import AbstractRouter


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
        with auth_factory.authenticate() as authenticate:
            status = await authenticate(login_data)
        return status
