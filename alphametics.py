"""Find solutions to alphametic equations.

alphametics.solve('SEND + MORE == MONEY')
'9567 + 1085 == 10652'

TODO: Support more complex equations.
"""

import operator
import re
from itertools import zip_longest, permutations


def solve(puzzle: str) -> str:  # -> Any | None:
    """_summary_

    Args:
        puzzle (_type_): _description_

    Returns:
        _type_: _description_
    """
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        # "//": operator.floordiv,
        # "%": operator.mod,
        # "**": operator.pow,
        "==": operator.eq,
    }

    words = re.findall("[A-Z]+", puzzle.upper())
    unique_characters = set("".join(words))
    operators = re.findall(r"[+\-*/%//=]+", puzzle)
    assert len(unique_characters) <= 10, "Too many letters"
    assert set(operators).issubset(set(operations.keys())), "Unsupported operator"
    assert operators.count("==") == 1, "Exactly one '==' is required"
    assert (
        operators.index("==") == len(operators) - 1 or operators.index("==") == 0
    ), "'==' must be at start or end of the equation"
    first_letters = {word[0] for word in words}
    n = len(first_letters)
    sorted_characters = "".join(first_letters) + "".join(
        unique_characters - first_letters
    )
    characters = tuple(ord(c) for c in sorted_characters)
    digits = tuple(ord(c) for c in "0123456789")
    zero = digits[0]

    for guess in permutations(digits, len(characters)):
        if zero not in guess[:n]:
            equation = puzzle.translate(dict(zip(characters, guess)))
            members = list(int(v) for v in re.findall(r"-?\d*\.?\d+", equation))
            results = list(zip_longest(members, operators))

            # Find position of '==' in equation. Could be 'a + b == c' or 'd == a + b + c', etc
            # But only allow one '==' and no fancy variations.

            for index, r in enumerate(results):
                x = operations[r[1]]
                y = x(r[0], results[index + 1][0]) if index + 1 < len(results) else None

                v = 1
            # if int(x) + int(y) == int(z):  # pylint: disable=W0123
            #    return equation
    return "No solution!!"


if __name__ == "__main__":
    import sys

    for puzz in sys.argv[1:]:
        print(puzz)
        solution = solve(puzz)
        if solution:
            print(solution)

# Copyright (c) 2009, Raymond Hettinger, All rights reserved.
# Ported to Python 3 and modified by Mark Pilgrim
# original: http://code.activestate.com/recipes/576615/
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 'AS IS'
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
