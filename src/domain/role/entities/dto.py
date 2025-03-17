from dataclasses import dataclass


@dataclass(frozen=True)
class RoleCreateDTO:
    name: str
    data: dict
