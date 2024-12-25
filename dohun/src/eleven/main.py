from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str) -> list:
    stones_list = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            nums = [int(x) for x in line.strip("\n").split(" ")]

    return np.array(nums)


def _iterate_stone(stone: int) -> list:
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        half_len_stone = int(len(str(stone)) / 2)
        return [int(str(stone)[:half_len_stone]), int(str(stone)[half_len_stone:])]
    else:
        return [stone * 2024]


def q1(stones_list: list, iterations: int = 25) -> int:
    for i in range(iterations):
        new_stones_list = []
        for stone in stones_list:
            new_stones_list += _iterate_stone(stone)
        stones_list = new_stones_list

    return len(stones_list)


def q2(stones_list: list, iterations: int = 75) -> int:
    stones_dict = Counter(stones_list)
    for i in range(iterations):
        new_stones_dict = {}
        for stone in stones_dict.keys():
            temp_stones_list = _iterate_stone(stone)
            for new_stone in temp_stones_list:
                if new_stone in new_stones_dict:
                    new_stones_dict[new_stone] += stones_dict[stone]
                else:
                    new_stones_dict[new_stone] = stones_dict[stone]
        stones_dict = new_stones_dict

    return sum(stones_dict.values())


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    stones_list = load_data(filename)
    print(q1(stones_list))
    print(q2(stones_list))
