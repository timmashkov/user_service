from fastapi import status

from infrastructure.common.base_entities.base_exception import BaseAPIException


class AuthenticationError(BaseAPIException):
    message = "Authentication Error"
    status_code = status.HTTP_404_NOT_FOUND
