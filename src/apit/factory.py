from typing import Generic
from typing import TypeVar

from apit.error import ApitUnsupportedTypeError

T = TypeVar("T")


class Factory(Generic[T]):
    factory_types: dict[str, type[T]] = {}

    @classmethod
    def register(cls, factory_type: str):
        def decorator_fn(decorated_cls: type[T]):
            cls.factory_types[factory_type] = decorated_cls
            return decorated_cls

        return decorator_fn

    @classmethod
    def create(cls, factory_type: str, *args, **kwargs) -> T:
        try:
            return cls.factory_types[factory_type](*args, **kwargs)
        except KeyError:
            raise ApitUnsupportedTypeError(factory_type)

    @classmethod
    def get_factory_types(cls) -> list[str]:
        return list(cls.factory_types.keys())
