def my_decorator(func):
    """_summary_

    Args:
        func (_type_): _description_
    """
    def wrapper(*args, **kwargs):
        print("Something is happening before the function is called.")
        result = func(*args, **kwargs)
        print("Something is happening after the function is called.")
        return result
    return wrapper

@my_decorator
def say_hello(name) -> None:
    """_summary_

    Args:
        name (_type_): _description_
    """
    print(f"Hello, {name}!")

say_hello("Alice")
