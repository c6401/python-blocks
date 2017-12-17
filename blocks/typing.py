from __future__ import unicode_literals
from typing import Dict, List, Text, Union

SimpleJson = Union[None, bool, float, Text, List, Dict]

# linters often don't support real recursion
_JsonRecursion = Union[
    None, bool, float, Text, List[SimpleJson], Dict[Text, SimpleJson],
]

Json = Union[
    None,
    bool,
    float,
    Text,
    List[_JsonRecursion],
    Dict[Text, _JsonRecursion],
]
