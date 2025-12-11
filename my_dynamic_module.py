"""_summary_

Returns:
    _type_: _description_
"""

from typing import Any


def greet(name) -> str:
    """_summary_

    Args:
        name (_type_): _description_

    Returns:
        str: _description_
    """
    return f"Hello, {name} from the dynamic module!"


class MyClass:
    """_summary_"""

    def __init__(self, value) -> None:
        self.value = value

    def get_value(self) -> Any:
        """_summary_

        Returns:
            Any: _description_
        """
        return self.value
