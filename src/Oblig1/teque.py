from typing import Optional, List
import sys


class Deque:
    def __init__(self, capacity: int):
        self._half = capacity // 4
        self._push_backs: int = 0
        self._push_fronts: int = 0
        self._data: List[Optional[int]] = [None] * ((capacity // 2) + 1)

    def push_front(self, value: int):
        self._data[self._half - self._push_fronts] = value
        self._push_fronts += 1

    def push_back(self, value: int):
        self._data[self._half + 1 + self._push_backs] = value
        self._push_backs += 1

    def pop_front(self) -> int:
        self._push_fronts -= 1
        return self._data[self._half - self._push_fronts]

    def pop_back(self) -> int:
        self._push_backs -= 1
        return self._data[self._half + 1 + self._push_backs]

    def __getitem__(self, key):
        return self._data[self._half - self._push_fronts + key + 1]

    def __len__(self):
        return self._push_fronts + self._push_backs


class Teque:
    def __init__(self, capacity: int):
        self._front = Deque(capacity)
        self._back = Deque(capacity)

    def push_front(self, value: int):
        self._front.push_front(value)
        if len(self._back) < len(self._front) - 1:
            self._back.push_front(self._front.pop_back())

    def push_back(self, value: int):
        self._back.push_back(value)
        if len(self._front) < len(self._back):
            self._front.push_back(self._back.pop_front())

    def push_middle(self, value: int):
        if len(self._back) < len(self._front):
            self._back.push_front(value)
        else:
            self._front.push_back(value)

    def __len__(self):
        return len(self._front) + len(self._back)

    def __getitem__(self, key):
        front_size = len(self._front)
        return self._front[key] if key < front_size else self._back[key - front_size]


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    myTeque = Teque(int(lines[0]))

    for line in lines[1: ]:
        command, argument = line.split(" ")
        if command == "push_back":
            myTeque.push_back(int(argument))
        elif command == "push_front":
            myTeque.push_front(int(argument))
        elif command == "push_middle":
            myTeque.push_middle(int(argument))
        elif command == "get":
            sys.stdout.write(f"{myTeque[int(argument)]}\n")


