from typing import Optional, List


class Deque:
    def __init__(self):
        self._CAPACITY = 10 ** 6
        self._push_backs: int = 0
        self._push_fronts: int = 0
        self._data: List[Optional[int]] = [None] * self._CAPACITY * 2

    def push_front(self, value: int):
        self._data[self._CAPACITY - self._push_fronts] = value
        self._push_fronts += 1

    def push_back(self, value: int):
        self._data[self._CAPACITY + 1 + self._push_backs] = value
        self._push_backs += 1

    def pop_front(self) -> int:
        self._push_fronts -= 1
        return self._data[self._CAPACITY - self._push_fronts]

    def pop_back(self) -> int:
        self._push_backs -= 1
        return self._data[self._CAPACITY + 1 + self._push_backs]

    def __getitem__(self, key):
        return self._data[self._CAPACITY - self._push_fronts + key + 1]  # test

    def __len__(self):
        return self._push_fronts + self._push_backs


class Teque:
    def __init__(self):
        self._front = Deque()
        self._back = Deque()

    def push_front(self, value: int):
        self._front.push_front(value)
        self._back.push_front(self._front.pop_back())

    def push_back(self, value: int):
        self._back.push_back(value)
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
    deque = Deque()
    deque.push_back(1)
    deque.push_front(2)
    print(deque[0], deque[1])
    print(deque.pop_front())
    print(deque[0])
