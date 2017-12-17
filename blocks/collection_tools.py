import random
from itertools import islice


MYPY = False
if MYPY:
    from decimal import Decimal
    from typing import (
        Any, Callable, Dict, Hashable, Iterable, List, Optional, Tuple,
        TypeVar, Union, Sequence, Text,
    )
    from .typing import Json

    T = TypeVar('T')
    NumberT = TypeVar('NumberT', int, float, Decimal)


def walk_json(
    json,  # type: Json
    dict_hook=lambda x: x,  # type: Callable[[Dict[Text, Json]], Any]
    list_hook=lambda x: x,  # type: Callable[[List[Json]], Any]
):  # type: (...) -> Any
    """
    >>> walk_json([{}], dict_hook=lambda d: {'a': 1}, list_hook=lambda l: l*2)
    [{'a': 1}, {'a': 1}]
    """
    if json is None:
        return json
    elif isinstance(json, (int, float)):
        return json
    elif isinstance(json, str):
        return json
    elif isinstance(json, list):
        return list_hook([
            walk_json(el, dict_hook=dict_hook)
            for el
            in json
        ])
    elif isinstance(json, dict):
        return dict_hook({
            k: walk_json(v, dict_hook=dict_hook)
            for k, v
            in json.items()
        })


def group_by(iterable, key):
    # type: (Iterable[T], Callable[[T], Hashable]) -> Dict[Hashable, List[T]]
    """
    >>> group_by(['futura', 'firra sans', 'helvetica'], lambda w: w[0])
    {'f': ['futura', 'firra sans'], 'h': ['helvetica']}
    """
    groups = {}  # type: Dict[Hashable, List[T]]
    for item in iterable:
        groups.setdefault(key(item), []).append(item)
    return groups


def window(iterable, size=2):
    # type: (Iterable[T], int) -> Iterable[Tuple[Optional[T], ...]]
    """
    >>> list(window([1, 2, 3, 4], 2))
    [(1, 2), (2, 3), (3, 4)]
    """
    iterable = iter(iterable)

    window = tuple(next(iterable) for i in range(size))
    yield window

    for item in iterable:
        window = tuple(islice(window, 1, None)) + (item,)
        yield window


def accumulate(iterable):
    # type: (Iterable[NumberT]) -> Iterable[NumberT]
    """
    >>> list(accumulate([1, 2, 3, 4]))
    [1, 3, 6, 10]
    """
    iterable = iter(iterable)

    accumulator = next(iterable)
    yield accumulator

    for item in iterable:
        accumulator += item
        yield accumulator


def weighted_choice(pairs):
    # type: (Sequence[Tuple[T, NumberT]]) -> Optional[T]
    """Randomly choose weighted element with from pairs of (element, weight).

    >>> from collections import Counter
    >>> test = [('a', 9), ('b', 5), ('c', 1)]
    >>> choiced = [weighted_choice(test) for i in range(999)]  # ~['b', 'a', 'a'
    >>> count = Counter(choiced)  # ~= Counter({'a': 599, 'b': 333, 'c': 67})
    >>> count['a'] > count['b'] > count['c']
    """
    items, weights = zip(*pairs)
    choice_position = random.uniform(0, float(sum(weights)))

    for item, position in zip(items, accumulate(weights)):
        if choice_position <= position:
            return item
