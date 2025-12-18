"""
Calculate factorial of n recursively with debug prints.

Demonstration of generator in list, unpacking list for print() param.
"""

from typing import Any, Generator


def fib(maxnum) -> Generator[int, Any, None]:
    """Calculate factorial of n recursively with debug prints."""
    a, b = 0, 1

    while a < maxnum:
        yield a
        a, b = b, a + b


if __name__ == "__main__":
    print(*list(fib(1000)), sep=", ", end="")
