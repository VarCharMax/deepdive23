"""Print methods and doc strings.
    Takes module, class, list, dictionary, or string."""

import inspect

def info(obj, spacing=10, collapse=1):
    """Print methods and doc strings.
    Takes module, class, list, dictionary, or string."""

    methodlist = [name for (name, method) in inspect.getmembers(obj, inspect.ismethod(obj))
         if not name.startswith('__')]

    processfunc = (lambda s: " ".join(s.split())) if collapse else (lambda s: s)

    print("\n".join([f"{method.ljust(spacing)} {processfunc(str(getattr(obj, method).__doc__))}"
                     for method in methodlist]) )

if __name__ == "__main__":
    print(info.__doc__)
