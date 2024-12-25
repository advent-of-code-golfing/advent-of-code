from src.utils import get_input_filename
from collections import Counter
import itertools
from functools import cache
import numpy as np
import copy
from pathlib import Path
from time import time


def load_data(filename: str) -> tuple:
    towels_list = list()
    target_towels = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            if line == "\n":
                continue
            if "," not in line:
                target_towels.append(line.strip())

            line = line.strip().split(", ")
            if len(line) > 1:
                towels_list += line

    towels_dict = {x: True for x in towels_list}
    return towels_dict, target_towels


# Bit grim, but need a global variable to make caching work. Maybe better to use frozendict?
towels_list = list()
dir = Path(__file__).parent / "input.txt"
with open(dir.__str__(), "r") as f:
    for line in f.readlines():
        if line == "\n":
            continue
        if "," not in line:
            continue

        line = line.strip().split(", ")
        if len(line) > 1:
            towels_list += line

towels_dict = {x: True for x in towels_list}


@cache
def recursively_find_all_towel_num(target_towel: str) -> int:
    sol = recursively_find_towels(target_towel)
    if "".join(sol) != target_towel:
        return 0
    if len(target_towel) == 0:
        return 0
    len_target = len(target_towel)
    successful_attempts = 0
    for i in range(1, min(len_target, 8) + 1):
        sub_string = target_towel[0:i]
        if sub_string in towels_dict.keys():
            if i == len_target:
                successful_attempts += 1
            else:
                successful_attempts += recursively_find_all_towel_num(target_towel[i:])

    return successful_attempts


@cache
def recursively_find_towels(target_towel: str) -> dict():
    """
    Try to have a memory by returning a dictionary instead
    """
    len_target = len(target_towel)
    # Max string length is 8
    for i in range(1, min(len_target, 8) + 1):
        sub_string = target_towel[0:i]
        if sub_string in towels_dict.keys():
            if i == len_target:
                return [sub_string]
            else:
                attempt = [sub_string] + recursively_find_towels(target_towel[i:])
                attempt_str = "".join(attempt)
                if attempt_str == target_towel:
                    return attempt
                else:
                    continue
    return []


def q1(target_towels: list) -> int:
    success = 0
    for i, target_towel in enumerate(target_towels):
        part_towel = recursively_find_towels(target_towel)
        attempt = "".join(part_towel)

        if attempt == target_towel:
            success += 1

    return success


def q2(target_towels: list) -> int:
    success = 0
    for i, target_towel in enumerate(target_towels):
        success += recursively_find_all_towel_num(target_towel)

    return success


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    _, target_towels = load_data(filename)
    print(q1(target_towels))
    print(q2(target_towels))
