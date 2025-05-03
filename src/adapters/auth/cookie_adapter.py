from typing import Literal, Optional, Union

from fastapi import Response

from application.config import settings


class CookieAdapter:
    def __init__(
        self,
        response: Response,
    ) -> None:
        self.response = response
        self.cookie_key: str = settings.COOKIE.cookie_key
        self.expiration: Union[int, float] = settings.COOKIE.expiration
        self.same_site: Literal["lax", "strict", "none"] = settings.COOKIE.same_site
        self.httponly: bool = settings.COOKIE.httponly
        self.secure: bool = settings.COOKIE.secure

    def set_auth_cookie(self, token: str, key: Optional[str] = None) -> None:
        self.response.set_cookie(
            key=key if key else self.cookie_key,
            value=token,
            httponly=self.httponly,
            max_age=self.expiration,
            secure=self.secure,
            samesite=self.same_site,
        )

    def delete_auth_cookie(self) -> None:
        self.response.delete_cookie(key=self.cookie_key)

    def refresh_auth_cookie(self, tokens: dict[str:str]) -> None:
        self.delete_auth_cookie()
        for key, value in tokens.items():
            self.set_auth_cookie(key=key, token=value)
