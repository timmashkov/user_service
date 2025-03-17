from application.config import settings
from application.server import ApiServer
from presentation.api.permission_router import PermissionRouter
from presentation.api.role_router import RoleRouter
from presentation.api.user_router import UserRouter

user_app = ApiServer(
    name=settings.NAME,
    routers=[
        UserRouter().api_router,
        RoleRouter().api_router,
        PermissionRouter().api_router,
    ],
    start_callbacks=[],
    stop_callbacks=[],
).app
