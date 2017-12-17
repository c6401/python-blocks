MYPY = False
if MYPY:
    from typing import Dict, Iterable, Optional, Text, TypeVar

    T = TypeVar('T')
    S = TypeVar('S')

class FrozenDict(dict):
    @classmethod
    def fromkeys(cls, keys, value=None):
        # type: (Iterable[T], Optional[S]) -> Dict[T, S]
        return cls((key, value) for key in keys)

    def __repr__(self):  # type: () -> Text
        return f'{self.__class__.__name__}({dict.__repr__(self)})'

    def __hash__(self):  # type: () -> int
        return hash((*self.items(),))

    def __setitem__(self, *args, **kwargs):  # type: ignore
        raise TypeError(f"'{self.__class__.__name__}' objects are immutable")

    __delitem__ = setdefault = update = pop = popitem = clear = __setitem__
