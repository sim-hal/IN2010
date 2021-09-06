import sys

from typing import Optional, List

myTree: List[Optional[int]] = [None] * 100
lines = sys.stdin.readlines()
kitten = int(lines[0])
for line in lines[1:]:
    split = line.split(" ")
    number_of_children = len(split) - 1
    parent = int(split[0])
    if parent == -1:
        break
    for i in range(number_of_children):
        child = int(split[1 + i])
        myTree[child] = parent
prev = kitten
sys.stdout.write(str(kitten))
while myTree[prev] is not None:
    prev = myTree[prev]
    sys.stdout.write(str(prev))


