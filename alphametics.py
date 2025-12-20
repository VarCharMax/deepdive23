"""Find solutions to alphametic equations.

alphametics.solve('SEND + MORE == MONEY')
'9567 + 1085 == 10652'

Modified to remove reliance on eval(), permit other operators besides addition,
and allow more flexibility in the equation structure.

I've kept the copyright notice from the original code at the bottom of this file.
But I don't know why people feel the need to include such notices in code like this.
It's just a brute force solution, and there are actual mathematical techniques for
solving these types of puzzles.
"""

import operator
import re
from itertools import permutations


def solve(puzzle: str) -> str:  # -> Any | None:
    """_summary_

    Args:
        puzzle (_type_): _description_

    Returns:
        _type_: _description_
    """

    def convert_val(tup: tuple[int, str]) -> int:
        if tup[1] == "-":
            return tup[0] * -1
        return tup[0]

    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "==": operator.eq,
    }

    words = re.findall("[A-Z]+", puzzle.upper())
    unique_characters = set("".join(words))
    operators = re.findall(
        r"[+\-*/%//=]+", puzzle
    )  # Each operator including '==' in sequence.

    assert len(unique_characters) <= 10, "Too many letters"
    assert set(operators).issubset(set(operations.keys())), "Unsupported operator"
    assert operators.count("==") == 1, "Exactly one '==' is required"
    assert (
        operators.index("==") == len(operators) - 1 or operators.index("==") == 0
    ), "'==' must be at start or end of the equation"

    # Find position of '==' in equation.
    # Could be 'a + b == c' or 'd == a + b + c', etc
    if operators.index("==") == 0:
        eq_pos = 0
    else:
        eq_pos = len(operators) - 1

    operators.remove("==")  # Remove '==' for calculation purposes.
    operators.insert(0, "")  # To align lists.
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

            # Extract all numbers from the translated equation
            members = list(int(v) for v in re.findall(r"-?\d*\.?\d+", equation))

            # Locate body and result based on position of '=='.
            if eq_pos == 0:  # '==' is at the start
                res = members[0]  # Result is leftmost value
                body = members[1:]
            else:  # '==' is at the end
                res = members[-1]
                body = members[:-1]

            # Deal with subtraction simply by negating next value.
            results = [convert_val(o) for o in zip(body, operators)]

            if int(res) == sum(results):
                return equation
    return "No solution!!"


if __name__ == "__main__":
    import sys

    puzzles = sys.argv[1:]
    if not puzzles:
        puzzles = [
            "SEND + MORE == MONEY",
            "TWO + TWO == FOUR",
            "BASE + BALL == GAMES",
            "SATURN + URANUS + NEPTUNE + PLUTO == PLANETS",
            "CROSS + ROADS == DANGER",
            "ZEROES + ONES == BINARY",
            "I + BB == ILL",
        ]
    for puzz in puzzles:
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
