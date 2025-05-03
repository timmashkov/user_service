from pydantic import BaseModel


class RefreshTokenModel(BaseModel):
    refresh_token: str
