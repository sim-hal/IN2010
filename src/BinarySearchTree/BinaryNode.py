from __future__ import annotations
from enum import Enum

import numpy as np
from typing import Optional, Union, List, Dict

from Infinity import _Infinity

Number = Union[int, float, _Infinity]
LOW = "low"
HIGH = "high"


class BinaryNode:

    def __init__(self, value: Number, parent: Optional[BinaryNode] = None):
        self._parent: Optional[BinaryNode] = parent
        self.value: Number = value
        self._children: Dict[str, Optional[BinaryNode]] = {LOW: None, HIGH: None}

    @property
    def _role(self) -> str:
        return LOW if self.value < self._parent.value else HIGH

    @property
    def low(self) -> Optional[BinaryNode]:
        return self._children[LOW]

    @property
    def high(self) -> Optional[BinaryNode]:
        return self._children[HIGH]

    @low.setter
    def low(self, value: Optional[BinaryNode]):
        self._children[LOW] = value
        if value is not None:
            value._parent = self

    @high.setter
    def high(self, value: Optional[BinaryNode]):
        self._children[HIGH] = value
        if value is not None:
            value._parent = self

    def find(self, value: Number) -> Optional[BinaryNode]:
        if value == self.value:
            return self
        child = self.low if value < self.value else self.high
        return child.find(value) if child is not None else None

    def insert(self, value: Number):
        children = self._children
        child = LOW if value < self.value else HIGH
        if children[child] is None:
            children[child] = BinaryNode(value, self)
        else:
            children[child].insert(value)

    def max_child(self) -> BinaryNode:
        return self if self.high is None else self.high.max_child()

    def min_child(self) -> BinaryNode:
        return self if self.low is None else self.low.min_child()

    def sort_children(self) -> List[Number]:
        sorted_lower = self.low.sort_children() if self.low is not None else []
        sorted_higher = self.high.sort_children() if self.high is not None else []
        return sorted_lower + [self.value] + sorted_higher

    def shortest_path(self) -> int:
        low_shortest = -1 if self.low is None else self.low.shortest_path()
        high_shortest = -1 if self.high is None else self.high.shortest_path()
        return min(low_shortest, high_shortest) + 1

    def delete(self):
        low = self.low
        high = self.high
        role = self._role
        if high is None:
            if role == LOW:
                self._parent.low = low
            else:
                self._parent.high = low
        elif low is None:
            if role == LOW:
                self._parent.low = high
            else:
                self._parent.high = high
        else:
            min_max = self.high.min_child()
            self.value = min_max.value
            min_max.delete()





