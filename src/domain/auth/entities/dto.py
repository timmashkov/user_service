from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class TokenDTO:
    password: str
    salt: str
    encoded_pass: Optional[str] = None


@dataclass(frozen=True)
class PayloadDTO:
    expiration: int
    iat: int
    scope: str
    sub: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LoginDTO:
    login: str
    password: str


@dataclass(frozen=True)
class LoginResult:
    access_token: str
    refresh_token: str


@dataclass(frozen=True)
class LogoutDTO:
    status: bool
