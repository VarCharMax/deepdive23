"""Calculate factorial of n recursively with debug prints.
Demonstration of recursion.
"""


def fac(n) -> int:
    """Calculate factorial of n recursively with debug prints."""

    print("n =", n)

    if n > 1:

        return n * fac(n - 1)

    print("end of the line")

    return 1


if __name__ == "__main__":
    print(fac(5))
