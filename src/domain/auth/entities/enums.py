from enum import Enum, auto


class TokenTypes(Enum):
    ACCESS: str = "access_token"
    REFRESH: str = "refresh_token"

    @property
    def description(self) -> str:
        if self == self.ACCESS:
            return self.ACCESS.value
        elif self == self.REFRESH:
            return self.REFRESH.value
        return ""


class AuthOptions(Enum):
    LOGIN = auto()
    LOGOUT = auto()
    CHECK_AUTH = auto()
    REFRESH_TOKEN = auto()
