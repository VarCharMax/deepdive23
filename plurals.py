"""_summary_

Returns:
Demonstration of closures, generators, custom iterators, loading re rules from config file.
"""

import re
from lazyrules import LazyRules


def build_match_and_apply_functions(pattern, search, replace):
    """_summary_

    Args:
        pattern (_type_): _description_
        search (_type_): _description_
        replace (_type_): _description_
    """

    def matches_rule(word) -> re.Match[str] | None:
        return re.search(pattern, word)

    def apply_rule(word) -> str:  # -> Any:
        return re.sub(search, replace, word)

    return (matches_rule, apply_rule)


def rules(
    rules_filename,
):  # -> Generator[tuple[Callable[..., Match[str] | None], Callabl...:
    """
    Docstring for rules

    :param rules_filename: Description
    """
    with open(rules_filename, encoding="utf-8") as pattern_file:
        for line in pattern_file:
            pattern, search, replace = line.split(None, 3)
            yield build_match_and_apply_functions(pattern, search, replace)


def plural(noun) -> str:
    """_summary_

    Args:
        noun (_type_): _description_

    Returns:
        _type_: _description_
    """

    for matches_rule, apply_rule in LazyRules():
        if matches_rule(noun):
            return apply_rule(noun)

    return ""


if __name__ == "__main__":
    import sys

    if sys.argv[1:]:
        cmd_args = sys.argv[1:2][0].split(" ")
        for a in cmd_args:
            print(plural(a))
    else:
        print(__doc__)
