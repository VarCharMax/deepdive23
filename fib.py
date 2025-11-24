"""Calculate factorial of n recursively with debug prints."""

def fib(n):
    """Calculate factorial of n recursively with debug prints."""

    print('n =',n)
    if n > 1:
        return n * fib(n - 1)
    else:
        print('end of the line')
        return 1


if __name__ == "__main__":
    print(fib(10))
