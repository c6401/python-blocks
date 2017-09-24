from operator import getitem, setitem
from typing import NamedTuple


class Field(NamedTuple):
    source: str = None
    field: 'Field' = None
    getter: callable = None
    setter: callable = None
    loader: callable = lambda x: x
    dumper: callable = lambda x: x
    
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


class Item(Field):
    getter = getitem
    setter = setitem


class Attr(Field):
    getter = getattr
    setter = setattr


class Map:
    def __init__(self, _default=Item, **fields):
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
