from src.utils import get_input_filename
from collections import Counter

import numpy as np
import copy


def load_data(filename: str) -> tuple[dict[int, list], list[list]]:
    rules_dict: dict[int, list] = {}
    updates_list: list[list] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            if "|" in line:
                before, after = (int(x) for x in line.strip("\n").split("|"))
                if before in rules_dict.keys():
                    rules_dict[before] = rules_dict[before] + [after]
                else:
                    rules_dict[before] = [after]
            elif len(line.strip("\n")) > 0:
                updates_list.append([int(x) for x in line.strip("\n").split(",")])

        return rules_dict, updates_list


def _check_if_update_good(
    rules_dict: dict[int, list], update: list[int]
) -> tuple[bool, int]:
    len_update = len(update)
    middle = int((len_update - 1) / 2)
    for i in range(len_update):
        num_to_check = update[i]

        if num_to_check not in rules_dict.keys():
            continue

        rules_after = rules_dict[num_to_check]
        before = update[:i]
        after = update[i + 1 :]
        for num_to_check in after:
            if num_to_check not in rules_after:
                return 0, update[middle]

        for num_to_check in before:
            if num_to_check in rules_after:
                return 0, update[middle]

    return 1, update[middle]


def _update_correct_iteration(rules_dict: dict[int, list], update: list[int]) -> tuple:
    len_update = len(update)
    middle = int((len_update - 1) / 2)
    for i in range(len_update):
        num_to_check = update[i]

        if num_to_check not in rules_dict.keys():
            continue

        rules_after = rules_dict[num_to_check]
        before = update[:i]

        for num_to_check in before:
            if num_to_check in rules_after:
                wrong_index = update.index(num_to_check)
                update[wrong_index], update[i] = update[i], update[wrong_index]
                return 0, update

    return 1, update[middle]


def q1(rules_dict: dict[int, list], updates_list: list[list]) -> int:
    count = 0
    for update in update_list:
        update_good, middle = _check_if_update_good(rules_dict, update)

        if update_good:
            count += middle

    return count


def q2(rules_dict: dict[int, list], updates_list: list[list]) -> int:
    count = 0
    for update in update_list:
        update_good, middle = _check_if_update_good(rules_dict, update)

        if update_good:
            continue

        while not update_good:
            update_good, update = _update_correct_iteration(rules_dict, update)

        count += update

    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    rules_dict, update_list = load_data(filename)
    print(q1(rules_dict, update_list))
    print(q2(rules_dict, update_list))
