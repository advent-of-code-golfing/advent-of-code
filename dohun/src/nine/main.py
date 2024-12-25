from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str) -> tuple:
    disk_representation = list()
    num_representation = list()
    evens = list()
    odds = list()
    with open(filename, "r") as f:
        line = f.read()
        for i, char in enumerate(line):
            char_num = int(char)
            num_representation.append(char_num)
            if i % 2 == 0:
                evens.append(char_num)
                k = i / 2
                for _ in range(char_num):
                    disk_representation.append(int(k))
            else:
                odds.append(char_num)
                for _ in range(char_num):
                    disk_representation.append(".")

    return disk_representation, num_representation, evens, odds


def q1(disk_representation: list) -> int:
    len_disk = len(disk_representation)

    first_dot = next(i for i in range(len_disk) if disk_representation[i] == ".")
    last_num = next(
        len_disk - j - 1
        for j in range(len_disk)
        if disk_representation[len_disk - j - 1] != "."
    )

    while last_num > first_dot:
        disk_representation[first_dot], disk_representation[last_num] = (
            disk_representation[last_num],
            disk_representation[first_dot],
        )

        first_dot = next(i for i in range(len_disk) if disk_representation[i] == ".")
        last_num = next(
            len_disk - j - 1
            for j in range(len_disk)
            if disk_representation[len_disk - j - 1] != "."
        )

    count = 0
    for i, num in enumerate(disk_representation):
        if num == ".":
            break
        count += i * num
    return count


def q2(
    disk_representation: list, num_representation: list, evens: list, odds: list
) -> int:
    space_taken = [0 for _ in range(len(odds))]

    for i in range(len(evens)):
        current_index_num = len(evens) - i - 1
        current_file_len = evens[current_index_num]
        current_first_file_loc = sum(num_representation[: current_index_num * 2])

        for current_space_num, current_space_available in enumerate(odds):
            current_space_available = (
                odds[current_space_num] - space_taken[current_space_num]
            )
            if current_space_available == 0:
                continue
            current_first_space_loc = (
                sum(num_representation[: current_space_num * 2 + 1])
                + space_taken[current_space_num]
            )
            if current_first_space_loc > current_first_file_loc:
                break

            if current_file_len < current_space_available:
                disk_representation[
                    current_first_space_loc : current_first_space_loc + current_file_len
                ] = [current_index_num for _ in range(current_file_len)]
                disk_representation[
                    current_first_file_loc : current_first_file_loc + current_file_len
                ] = ["." for _ in range(current_file_len)]
                space_taken[current_space_num] += current_file_len

                break

            if current_file_len == current_space_available:
                disk_representation[
                    current_first_space_loc : current_first_space_loc + current_file_len
                ] = [current_index_num for _ in range(current_file_len)]
                disk_representation[
                    current_first_file_loc : current_first_file_loc + current_file_len
                ] = ["." for _ in range(current_file_len)]
                space_taken[current_space_num] += current_file_len

                break

        print(current_index_num)

    count = 0
    for i, num in enumerate(disk_representation):
        if num == ".":
            continue
        count += i * num

    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    disk_representation, num_representation, evens, odds = load_data(filename)
    # print(q1(disk_representation))
    print(q2(disk_representation, num_representation, evens, odds))
