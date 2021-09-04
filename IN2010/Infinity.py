

class _Infinity:

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __ge__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __eq__(self, other):
        return False

    def __add__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __mul__(self, other):
        if other == 0:
            raise Exception("0 * INFINITY is ambiguous")
        return self

    def __str__(self):
        return "INFINITY"

    def __repr__(self):
        return str(self)

    def __radd__(self, other):
        return self

    def __rmul__(self, other):
        if other == 0:
            raise Exception("0 * INFINITY is ambiguous")
        return self

    def __truediv__(self, other):
        return self

    def __rtruediv__(self, other):
        return 0


INFINITY = _Infinity()


if __name__ == "__main__":
    print(INFINITY)
    print(INFINITY < 3)
    print(5 < INFINITY)
    print(5 + INFINITY)
    print(INFINITY + 5)
    print(INFINITY/5)
    print(5/INFINITY)


