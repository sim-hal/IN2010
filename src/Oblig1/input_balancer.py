import sys

from typing import Optional, List


def order_array(arr: list):
    if len(arr) < 2:
        return arr

    middle = len(arr) // 2

    left = order_array(arr[:middle])
    right = order_array(arr[middle + 1:])

    return [arr[middle]] + left + right


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    input_list: List[Optional[int]] = [int(i) for i in lines]

    output_list = order_array(input_list)

    for i in output_list:
        sys.stdout.write(f"{i}\n")

