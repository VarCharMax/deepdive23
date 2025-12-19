"""_summary_

Demontration of property pattern in Python.
"""


class Contact(object):
    """_summary_

    Args:
        object (_type_): _description_
    """

    def __init__(
        self, first_name=None, last_name=None, display_name=None, email=None
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.display_name = display_name
        self.email = email

    def print_info(self) -> None:
        """_summary_"""
        print(self.display_name, "<" + self.email + ">")

    def __set_email(self, value) -> None:
        """_summary_"""
        if "@" not in value:
            raise Exception("This doesn't look like an email address.")
        self._email = value

    def __get_email(self) -> str:
        """_summary_"""
        return self._email

    email = property(__get_email, __set_email)


if __name__ == "__main__":
    contact = Contact(
        first_name="John",
        last_name="Doe",
        display_name="John Doe",
        email="john.doe@example.com",
    )

    contact.print_info()
