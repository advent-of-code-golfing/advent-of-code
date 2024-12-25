from src.utils import get_input_filename
from collections import Counter

import numpy as np
import copy


def load_data(filename: str) -> tuple[dict[int, list], list[list]]:
    ans_list = []
    x_list = []
    with open(filename, "r") as f:
        for line in f.readlines():
            ans, x = line.strip("\n").split(":")
            ans_list.append(int(ans))
            x_list.append([int(z) for z in x.strip().split(" ")])
        return ans_list, x_list


def _get_all_possible_values_recursive(x_s: list):
    if len(x_s) == 2:
        return [x_s[0] + x_s[1], x_s[0] * x_s[1]]
    else:
        return _get_all_possible_values_recursive(
            [x_s[0] * x_s[1]] + x_s[2:]
        ) + _get_all_possible_values_recursive([x_s[0] + x_s[1]] + x_s[2:])


def q1(ans_list: list[int], x_list: list[list]) -> int:
    count = 0

    for ans, x_s in zip(ans_list, x_list):
        all_poss_values = _get_all_possible_values_recursive(x_s)
        if ans in all_poss_values:
            count += ans

    return count


def _concatenate(x_1: int, x_2: int):
    return int(str(x_1) + str(x_2))


def _get_all_possible_values_recursive_part2(x_s: list):
    if len(x_s) == 2:
        return [x_s[0] + x_s[1], x_s[0] * x_s[1], _concatenate(x_s[0], x_s[1])]
    else:
        op_1 = _get_all_possible_values_recursive_part2([x_s[0] * x_s[1]] + x_s[2:])
        op_2 = _get_all_possible_values_recursive_part2([x_s[0] + x_s[1]] + x_s[2:])
        op_3 = _get_all_possible_values_recursive_part2(
            [_concatenate(x_s[0], x_s[1])] + x_s[2:]
        )

        return op_1 + op_2 + op_3


def q2(ans_list: list[int], x_list: list[list]) -> int:
    count = 0

    for ans, x_s in zip(ans_list, x_list):
        all_poss_values = _get_all_possible_values_recursive_part2(x_s)
        if ans in all_poss_values:
            count += ans
    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    ans_list, x_list = load_data(filename)
    print(q1(ans_list, x_list))
    print(q2(ans_list, x_list))
