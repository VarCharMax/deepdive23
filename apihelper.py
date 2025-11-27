"""Print methods and doc strings.
    Takes module, class, list, dictionary, or string."""

import inspect

def info(obj, spacing=10, collapse=1):
    """ Print methods and doc strings.
        Takes module, class, list, dictionary, or string.

        Args:
            obj (_type_): _description_
            spacing (int, optional): _description_. Defaults to 10.
            collapse (int, optional): _description_. Defaults to 1.
    """

    # This is the closest I can get to the author's original intent in Py3.
    # Callable doesn't filter out the __< >__ methods.
    methodlist = [n for (n, v) in inspect.getmembers(obj) if callable(v) and not n.startswith('__')]

    processfunc = (lambda s: " ".join(s.split())) if collapse else (lambda s: s)

    print("\n".join([f"{method.ljust(spacing)} {processfunc(str(getattr(obj, method).__doc__))}"
                     for method in methodlist ]))

if __name__ == "__main__":
    print(info.__doc__)
