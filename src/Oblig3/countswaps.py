from typing import List
from countcompares import CountCompares

class CountSwaps(List[CountCompares]):
    swaps = 0
    def swap(self, i, j):
        self.swaps += 1
        self[i], self[j] = self[j], self[i]
