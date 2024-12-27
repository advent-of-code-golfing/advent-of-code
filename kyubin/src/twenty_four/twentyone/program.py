from copy import deepcopy
from collections import Counter
from enum import StrEnum
from functools import cache

from src.common import Vector
from src.utils import get_input_filename

"""
NUMPAD:
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

KEYPAD:
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+

PART 2:
If we say have the pattern 02

1: <A^A
2: v<<A>>^A
3. <vA 
"""

NUMPAD: dict[str, Vector] = {
    "A": Vector(3, 2),
    "0": Vector(3, 1),
    "1": Vector(2, 0),
    "2": Vector(2, 1),
    "3": Vector(2, 2),
    "4": Vector(1, 0),
    "5": Vector(1, 1),
    "6": Vector(1, 2),
    "7": Vector(0, 0),
    "8": Vector(0, 1),
    "9": Vector(0, 2),
}

KEYPAD: dict[str, Vector] = {
    "A": Vector(0, 2),
    "^": Vector(0, 1),
    "<": Vector(1, 0),
    "v": Vector(1, 1),
    ">": Vector(1, 2),
}


class Lookup(StrEnum):
    KEY = "KEY"
    NUM = "NUM"


def load_data(filename: str) -> list[str]:
    lines: list[str] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            lines.append(line.strip())

    return lines


def generate_pattern(vec: Vector, left_right_first: bool) -> str:
    pattern = ""

    col_pattern = "<" if vec.col < 0 else ">"
    row_pattern = "^" if vec.row < 0 else "v"

    if left_right_first:
        pattern += col_pattern * abs(vec.col)
        pattern += row_pattern * abs(vec.row)
    else:
        pattern += row_pattern * abs(vec.row)
        pattern += col_pattern * abs(vec.col)

    return pattern


@cache
def get_strokes_from_vector(start: Vector, end: Vector, lookup: Lookup) -> str:
    # Let's say do right/left first by default
    # Left is furthest away from A. If possible, we want to do this FIRST
    # Right is close to A. We want to do this last

    vec = end - start

    if lookup == Lookup.NUM:
        if start.row == 3 and end.col == 0:
            # Must be up down first
            return generate_pattern(vec, False)
        if start.col == 0 and end.row == 3:
            # Must be left right first
            return generate_pattern(vec, True)
    if lookup == Lookup.KEY:
        if start.row == 0 and end.col == 0:
            # Must be up down first
            return generate_pattern(vec, False)
        if start.col == 0 and end.row == 0:
            # Must be left right first
            return generate_pattern(vec, True)

    # If vec.col < 0, pattern is "<"
    # This is far away so we want to do this first
    if vec.col < 0:
        return generate_pattern(vec, True)
    else:
        # If pattern is ">", this is close to A
        # so we want to do left right later
        return generate_pattern(vec, False)


def get_keypad_strokes(data: str, lookup: Lookup = Lookup.KEY) -> str:
    if len(data) == 1:
        return "A"
    if lookup == Lookup.KEY:
        lookup_dict = KEYPAD
    elif lookup == Lookup.NUM:
        lookup_dict = NUMPAD
    cur = lookup_dict[data[0]]
    strokes = ""
    for n in data[1:]:
        next_vec = lookup_dict[n]
        strokes += get_strokes_from_vector(cur, next_vec, lookup)
        strokes += "A"
        cur = next_vec
    return strokes


def get_user_stokes(data: str, layers: int, verbose: bool = False) -> str:
    # First robot
    cur = get_keypad_strokes("A" + data, Lookup.NUM)
    # Second robot

    for i in range(layers):
        if verbose:
            print(i, cur)
        cur = get_keypad_strokes("A" + cur, Lookup.KEY)
    return cur


def get_n_keypad_strokes(data: str, layers: int, verbose: bool = False) -> str:
    for i in range(layers):
        if verbose:
            print(i, data, len(data))
        data = get_keypad_strokes("A" + data, Lookup.KEY)
    return data


@cache
def get_sequence_recursive(line: str, iterations: int, first: bool) -> str:
    if iterations == 0:
        return line

    if first is True and line.startswith("A") is False:
        line = "A" + line

    if line == "AA":
        return "A"

    line_split = line.strip("A").split("A")
    for i in range(len(line_split)):
        line_split[i] = "A" + line_split[i] + "A"

    # print(line_split)

    if len(line_split) > 1:
        res = ""
        for i, line in enumerate(line_split):
            if not line:
                continue
            cur_res = get_sequence_recursive(line, iterations, i == 0)
            res += cur_res
            # print(line, cur_res)
        return res

    pattern = get_keypad_strokes(line)

    return get_sequence_recursive(pattern, iterations - 1, first)


@cache
def get_next_patterns(pattern: str) -> dict[str, int]:
    pattern = get_keypad_strokes(pattern)
    pattern = "A" + pattern
    counts: dict[str, int] = Counter()
    for l1, l2 in zip(pattern, pattern[1:]):
        counts[l1 + l2] += 1
    return counts


def get_sequence_count(line: str, iterations: int) -> int:
    counts: dict[str, int] = Counter()
    for l1, l2 in zip(line, line[1:]):
        counts[l1 + l2] += 1

    prev = counts
    # print(counts)

    for i in range(iterations):
        # print(f"Iteration {i + 1}")
        cur: dict[str, int] = Counter()
        for k, v in prev.items():
            patterns = get_next_patterns(k)
            for k2, v2 in patterns.items():
                cur[k2] += v * v2

        # print(line, i + 1, sum(cur.values()))
        prev = cur

    return sum(cur.values())


def solve_part_one(data: list[str]) -> int:
    tot = 0
    for line in data:
        res = get_user_stokes(line, 2)
        tot += len(res) * int(line.rstrip("A"))
    return tot


def solve_part_two(data: list[str]) -> int:
    total = 0

    for line in data:
        # print(line)
        keypad_strokes = get_user_stokes(line, 0)
        initial_steps = get_sequence_count("A" + keypad_strokes, 25)
        print(line, keypad_strokes, initial_steps)
        total += int(line.rstrip("A")) * initial_steps

    return total


def run(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)

    if test:
        print("------------PART ONE------------")
        print(solve_part_one(deepcopy(data)))
        print("------------PART TWO------------")
        print(solve_part_two(deepcopy(data)))
    else:
        print("------------PART ONE------------")
        print(solve_part_one(deepcopy(data)))
        print("------------PART TWO------------")
        print(solve_part_two(deepcopy(data)))


if __name__ == "__main__":
    run(False)
