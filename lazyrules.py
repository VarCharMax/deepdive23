"""_summary_

Raises:
    StopIteration: _description_

Returns:
    _type_: _description_
"""

import re
from typing import Self


class LazyRules:
    """_summary_

    Raises:
        StopIteration: _description_
        StopIteration: _description_

    Returns:
        _type_: _description_
    """

    rules_filename = "plural-rules.txt"

    def __init__(self) -> None:
        self.pattern_file = open(self.rules_filename, encoding="utf-8")
        self.cache = []
        self.cache_index = 0

    def __iter__(self) -> Self:
        self.cache_index = 0
        return self

    def __next__(self):# -> Any | tuple[Callable[..., Match[str] | None], Callable[.....:# -> Any | tuple[Callable[..., Match[str] | None], Callable[.....:# -> Any | tuple[Callable[..., Match[str] | None], Callable[.....:
        self.cache_index += 1
        if len(self.cache) >= self.cache_index:
            return self.cache[self.cache_index - 1]
        if self.pattern_file.closed:
            raise StopIteration
        line = self.pattern_file.readline()
        if not line:
            self.pattern_file.close()
            raise StopIteration

        pattern, search, replace = line.split(None, 3)
        funcs = self.__build_match_and_apply_functions(pattern, search, replace)
        self.cache.append(funcs)
        return funcs

    def __build_match_and_apply_functions(self, pattern, search, replace):
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
