"""_summary_"""

from typing import Self


class Fib:
    """_summary_"""

    def __init__(self, max_num) -> None:
        self.max = max_num
        self.a = 0
        self.b = 0

    def __iter__(self) -> Self:
        self.a = 0
        self.b = 1
        return self

    def __next__(self) -> int:
        fib = self.a
        if fib > self.max:
            raise StopIteration
        self.a, self.b = self.b, self.a + self.b
        return fib
