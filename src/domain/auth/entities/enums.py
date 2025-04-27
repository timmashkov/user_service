from enum import Enum


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
