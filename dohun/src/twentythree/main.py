from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str) -> list:
    return np.array(nums)


def q1(stones_list: list, iterations: int = 25) -> int:
    return len(stones_list)


def q2(stones_list: list, iterations: int = 75) -> int:
    return sum(stones_dict.values())


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    stones_list = load_data(filename)
    print(q1(stones_list))
    print(q2(stones_list))
