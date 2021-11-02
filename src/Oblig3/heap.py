from countswaps import CountSwaps

def bubble_down(A: CountSwaps, i: int, n: int):
    gr = i
    left = 2 * gr + 1
    right = 2 * gr + 2
    if left < n and A[gr] < A[left]:
        gr, left = left, gr
    if right < n and A[gr] < A[right]:
        gr, right = right, gr
    if i != gr:
        A.swap(i, gr)
        bubble_down(A, gr, n)


def build_heap(A: CountSwaps):
    n = len(A)
    for i in range(n // 2, 0, -1):
        bubble_down(A, i, n)    
    return A  


def heap_sort(A: CountSwaps) -> CountSwaps:
    if not A:
        return A
    n = len(A)
    build_heap(A)
    for i in range(n - 1, 0, -1):
        A.swap(0, i)
        bubble_down(A, 0, i)
    return A



def sort(A: CountSwaps) -> CountSwaps:
    return heap_sort(A)

