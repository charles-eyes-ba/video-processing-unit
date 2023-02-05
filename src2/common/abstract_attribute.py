from typing import cast, Any, Callable, TypeVar

class DummyAttribute:
    pass

R = TypeVar('R')
def abstract_attribute(obj: Callable[[Any], R] = None):
    _obj = cast(Any, obj)
    if obj is None:
        _obj = DummyAttribute()
    _obj.__is_abstract_attribute__ = True
    return cast(R, _obj)