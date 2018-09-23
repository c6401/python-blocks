from functools import partial
from operator import getitem, setitem
from typing import Any, Callable, NamedTuple, Optional


class Field(NamedTuple):
    source: Optional[str] = None
    field: Optional['Field'] = None
    getter: Optional[Callable] = None
    setter: Optional[Callable] = None
    loader: Callable = lambda x: x
    dumper: Callable = lambda x: x

    def load(self, instance):
        result = self.getter(instance, self.source)
        if self.field:
            result = self.field.load(result)
        return self.loader(result)

    def dump(self, instance, value):
        value = self.dumper(value)

        if self.field:
            self.field.dump(
                self.getter(instance, self.source),
                value,
            )
        else:
            self.setter(instance, self.source, value)


item = partial(Field, getter=getitem, setter=setitem)
attr = partial(Field, getter=getattr, setter=setattr)


class Map:
    def __init__(self, _default=item, **fields):
        self.fields = {
            name: _default(field) if isinstance(field, str) else field
            for name, field
            in fields.items()
        }

    def load(self, instance):
        return {
            name: field.load(instance)
            for name, field
            in self.fields.items()
        }

    def dump(self, instance, value):
        for name, field in self.fields.items():
            field.dump(instance, value[name])
