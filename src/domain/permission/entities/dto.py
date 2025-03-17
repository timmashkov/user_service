from dataclasses import dataclass


@dataclass(frozen=True)
class PermissionCreateDTO:
    name: str
    layer: str
    data: dict
