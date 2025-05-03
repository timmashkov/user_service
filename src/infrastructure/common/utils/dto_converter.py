from dataclasses import asdict
from typing import Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def dto_to_pydantic(dto: object, pydantic_model: Type[T]) -> T:
    """Конвертирует любой dataclass DTO в Pydantic модель."""
    return pydantic_model(**asdict(dto))
