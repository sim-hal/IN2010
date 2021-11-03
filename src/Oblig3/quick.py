import typing
from countswaps import CountSwaps


def choose_pivot(A: CountSwaps, low: int, high: int):
    mid = (low + high) // 2
    if A[mid] < A[low]:
        if A[low] < A[high]:
            return low
        elif A[high] < A[mid]:
            return mid
        else:
            return high
    else:
        if A[high] < A[low] :
            return low
        elif A[mid] < A[high]:
            return mid
        else:
            return high


def partition(A: CountSwaps, low: int, high: int):
    p = choose_pivot(A, low, high)
    A.swap(p, low)
    pivot = A[low]
    left = low+1
    right = high

    while left <= right:
        while left <= right and A[left] <= pivot:
            left += 1
        while right >= left and A[right] >= pivot:
            right -= 1
        if left < right:
            A.swap(left, right)
    A.swap(low, right)
    return right


def quicksort(A: CountSwaps, low: int, high: int):
    if low >= high:
        return
    p = partition(A, low, high)
    quicksort(A, low, p-1)
    quicksort(A, p+1, high)


def sort(A: CountSwaps):
    quicksort(A, 0, len(A)-1)
    return A
