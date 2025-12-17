"""_summary_

Returns:
    _type_: _description_
"""

import re


def build_match_and_apply_functions(pattern, search, replace):
    """_summary_

    Args:
        pattern (_type_): _description_
        search (_type_): _description_
        replace (_type_): _description_
    """

    def matches_rule(word):  # -> Any:# -> Any:
        return re.search(pattern, word)

    def apply_rule(word):  # -> Any:
        return re.sub(search, replace, word)

    return (matches_rule, apply_rule)


patterns = (
    ("[sxz]$", "$", "es"),
    ("[^aeioudgkprt]h$", "$", "es"),
    ("(qu|[^aeiou])y$", "y$", "ies"),
    ("$", "$", "s"),
)


rules = []

rules = [
    build_match_and_apply_functions(pattern, search, replace)
    for (pattern, search, replace) in patterns
]


def plural(noun):  # -> Any | None:
    """_summary_

    Args:
        noun (_type_): _description_

    Returns:
        _type_: _description_
    """
    for matches_rule, apply_rule in rules:
        if matches_rule(noun):
            return apply_rule(noun)


if __name__ == "__main__":
    import sys

    if sys.argv[1:]:
        print(plural(sys.argv[1]))
    else:
        print(__doc__)

# with open("plural4-rules.txt", encoding="utf-8") as pattern_file:
#    for line in pattern_file:
#        pattern, search, replace = line.split(None, 3)
#        rules.append(build_match_and_apply_functions(pattern, search, replace))
