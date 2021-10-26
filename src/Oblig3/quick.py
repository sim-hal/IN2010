
def choose_pivot(A, low, high):
    if A[low] > A[len(A)//2]:
        if A[low] < A[high]:
            return low
        elif A[len(A)//2] > A[high]:
            return len(A)//2
        else:
            return high
    else:
        if A[low] > A[high]:
            return low
        elif A[len(A)//2] < A[high]:
            return len(A)//2
        else:
            return high


def partition(A, low, high):
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

def quicksort(A, low: int, high: int):
    if low >= high:
        return
    p = partition(A, low, high)
    quicksort(A, low, p-1)
    quicksort(A, p+1, high)


def sort(A):
    print("IN QUICKSORT")
    quicksort(A, 0, len(A)-1)
    return A
