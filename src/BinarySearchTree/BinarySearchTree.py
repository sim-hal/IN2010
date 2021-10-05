from __future__ import annotations

from BinaryNode import BinaryNode, Number
from typing import List, Optional
from Infinity import INFINITY
import numpy as np


class BinarySearchTree:
    def __init__(self, value: Number):
        self.root = BinaryNode(value)

    @classmethod
    def _from_binary_node(cls, binary_node: BinaryNode) -> BinarySearchTree:
        instance = cls(0)
        instance.root = binary_node
        return instance

    def insert(self, value: Number):
        """
        Inserts value correctly into tree
        :param value: value to insert
        """
        self.root.insert(value)

    def max(self) -> Number:
        """
        :return: the largest number in the tree
        """
        return self.root.max_child().value

    def min(self) -> Number:
        """
        :return: the smallest number in the tree
        """
        return self.root.min_child().value

    def to_sorted_list(self) -> List[Number]:
        return self.root.sort_children()

    def _find(self, value: Number) -> Optional[BinaryNode]:
        return self.root.find(value)

    def delete(self, value: Number):
        """
        Deletes first instance of value
        :param value: Number to delete from tree
        """
        self._find(value).delete()

    def subtree(self, value: Number) -> Optional[BinarySearchTree]:
        """
        :param value: value to be root in subtree
        :return: subtree of this tree, with the provided value as root. None if value is not in tree
        """
        root = self._find(value)
        return self._from_binary_node(root) if root is not None else None
    
    def height(self) -> int:
        return self.root.height


if __name__ == "__main__":
    bst = BinarySearchTree(0.5)
    random_numbers = np.random.random(200)
    for v in random_numbers:
        bst.insert(v)
    before_deletion = bst.to_sorted_list()
    print(before_deletion[99], before_deletion[100])
    bst.delete(before_deletion[100])
    after_deletion = bst.to_sorted_list()
    print(after_deletion[99], after_deletion[100])
    bst.insert(INFINITY)
    print(bst.to_sorted_list())
    print(bst.height())
