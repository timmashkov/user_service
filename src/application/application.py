from application.config import settings
from application.container import Container
from application.server import ApiServer
from presentation.api.routers.auth_router import AuthRouter
from presentation.api.routers.permission_router import PermissionRouter
from presentation.api.routers.role_router import RoleRouter
from presentation.api.routers.user_router import UserRouter

user_app = ApiServer(
    name=settings.NAME,
    routers=[
        UserRouter().api_router,
        RoleRouter().api_router,
        PermissionRouter().api_router,
        AuthRouter().api_router,
    ],
    start_callbacks=[
        Container.broker_process_manager().start_consuming,
        Container.rabbit_manager().connect,
        Container.rabbit_manager().init_queues,
    ],
    stop_callbacks=[Container.broker_process_manager().stop_consuming],
).app
