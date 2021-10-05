from __future__ import annotations

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
        if self._parent == None:
            return "root"
        return LOW if self.value < self._parent.value else HIGH

    @property
    def low(self) -> Optional[BinaryNode]:
        return self._children[LOW]

    @property
    def high(self) -> Optional[BinaryNode]:
        return self._children[HIGH]

    @property
    def height(self) -> int:
        lower = self.low.height if self.low is not None else -1
        higher = self.high.height if self.high is not None else -1
        return max(lower, higher) + 1

    @property
    def depth(self) -> int:
        depth = 0
        current = self
        while current._parent is not None:
            current = current._parent
            depth += 1
        return depth

    @property
    def _balance_factor(self) -> int:
        return self.low.height - self.high.height

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
        if children[child] is not None: 
            children[child].insert(value)
        else:
            children[child] = BinaryNode(value, self)

    def max_child(self) -> BinaryNode:
        return self if self.high is None else self.high.max_child()

    def min_child(self) -> BinaryNode:
        return self if self.low is None else self.low.min_child()

    def sort_children(self) -> List[Number]:
        sorted_lower = self.low.sort_children() if self.low is not None else []
        sorted_higher = self.high.sort_children() if self.high is not None else []
        return sorted_lower + [self.value] + sorted_higher

    def shortest_path(self) -> int:
        shortest = 0
        current_row = [self]
        while None not in current_row:
            current_row = [current_row[i // 2].low if i % 2 == 0 else current_row[i // 2].high for i in range(2 ** shortest)]
            shortest += 1
        return shortest

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
    
    def left_rotate(self):
        y = self.high
        x = y.low

        y.low = self
        self.high = t_1
    
    def right_rotate(self):
        y = self.low
        x = y.high

        y.high = self
        self.low = t_1

    def balance(self):
        if self._balance_factor < -1:
            if self.high.balance_





