from heapq import heappush, heappop
import sys


def heap_balancer(heap):
    """Print out the values in a heap in order to achieve a binary sorted tree"""
    if len(heap) == 1:
        sys.stdout.write(f"{heappop(heap)}\n")
    if len(heap) == 2:
        a = heappop(heap)
        sys.stdout.write(f"{heappop(heap)}\n")
        sys.stdout.write(f"{a}\n")
    else:
        left = []
        right = []

        heap_len = len(heap)

        for _ in range(heap_len//2):
            heappush(left, heappop(heap))

        sys.stdout.write(f"{heappop(heap)}\n")

        for _ in range(heap_len//2 - 1 + heap_len % 2):
            heappush(right, heappop(heap))

        heap_balancer(left)
        heap_balancer(right)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    h = []
    for line in lines:
        heappush(h, int(line))
    heap_balancer(h)
