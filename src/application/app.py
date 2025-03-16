from application.config import settings
from application.server import ApiServer
from presentation.api.user_router import UserRouter

user_app = ApiServer(
    name=settings.NAME,
    routers=[UserRouter().api_router],
    start_callbacks=[],
    stop_callbacks=[],
).app
