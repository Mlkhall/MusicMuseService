from typing import Annotated, TypeVar
from enum import StrEnum
from pydantic import WrapValidator
from pydantic_core import PydanticUseDefault


class Statuses(StrEnum):
    active = "active"
    inactive = "inactive"
    deleted = "deleted"
    moderation = "moderation"


def _empty_str_to_default(v, handler, _):
    if isinstance(v, str) and v == '':
        raise PydanticUseDefault
    return handler(v)


T = TypeVar('T')
EmptyStrToDefault = Annotated[T, WrapValidator(_empty_str_to_default)]
