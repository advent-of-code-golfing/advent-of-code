from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str) -> tuple[dict[int, list], list[list]]:
    all_strs = ""
    locations = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            all_strs += line.strip("\n")
        unique_chars = set(all_strs)
        unique_char_dict = dict(zip(unique_chars, range(len(unique_chars))))

        for char, num in unique_char_dict.items():
            if unique_char_dict[char] == 0:
                if char != ".":
                    unique_char_dict["."], unique_char_dict[char] = (
                        0,
                        unique_char_dict["."],
                    )
                break

    with open(filename, "r") as f:
        for line in f.readlines():
            locations.append([unique_char_dict[x] for x in line.strip("\n")])

        return np.array(locations), unique_char_dict


def check_conditions(loc: tuple, operation: tuple, map_len: tuple) -> bool:
    row_loc, col_loc = loc[0], loc[1]
    row_op, col_op = operation[0], operation[1]
    row_len_map, col_len_map = map_len[0], map_len[1]

    row_ok = row_loc + row_op < row_len_map and row_loc + row_op >= 0
    col_ok = col_loc + col_op < col_len_map and col_loc + col_op >= 0

    return row_ok and col_ok


def q1(locations: np.array, unique_char_dict: dict()) -> int:
    nodes_array = np.zeros_like(locations)
    row_len_map = len(locations)
    col_len_map = len(locations[0])

    for char in unique_char_dict.keys():
        if char == ".":
            continue

        num = unique_char_dict[char]
        coordinates = np.where(locations == num)
        coords_list = [(x, y) for x, y in zip(coordinates[0], coordinates[1])]

        for loc_pair in itertools.combinations(coords_list, 2):
            (row_loc_1, col_loc_1), (row_loc_2, col_loc_2) = loc_pair
            row_op = row_loc_2 - row_loc_1
            col_op = col_loc_2 - col_loc_1

            if check_conditions(
                (row_loc_2, col_loc_2), (row_op, col_op), (row_len_map, col_len_map)
            ):
                nodes_array[row_loc_2 + row_op, col_loc_2 + col_op] = 1

            if check_conditions(
                (row_loc_1, col_loc_1), (-row_op, -col_op), (row_len_map, col_len_map)
            ):
                nodes_array[row_loc_1 - row_op, col_loc_1 - col_op] = 1

    return np.sum(nodes_array == 1)


def q2(locations: np.array, unique_char_dict: dict()) -> int:
    nodes_array = np.zeros_like(locations)
    row_len_map = len(locations)
    col_len_map = len(locations[0])

    for char in unique_char_dict.keys():
        if char == ".":
            continue

        num = unique_char_dict[char]
        coordinates = np.where(locations == num)
        coords_list = [(x, y) for x, y in zip(coordinates[0], coordinates[1])]

        for loc_pair in itertools.combinations(coords_list, 2):
            (row_loc_1, col_loc_1), (row_loc_2, col_loc_2) = loc_pair
            row_op = row_loc_2 - row_loc_1
            col_op = col_loc_2 - col_loc_1

            i = 0
            while check_conditions(
                (row_loc_2, col_loc_2),
                (i * row_op, i * col_op),
                (row_len_map, col_len_map),
            ):
                nodes_array[row_loc_2 + i * row_op, col_loc_2 + i * col_op] = 1
                i += 1

            i = 0
            while check_conditions(
                (row_loc_1, col_loc_1),
                (-i * row_op, -i * col_op),
                (row_len_map, col_len_map),
            ):
                nodes_array[row_loc_1 - i * row_op, col_loc_1 - i * col_op] = 1
                i += 1

    return np.sum(nodes_array == 1)


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    locations, unique_char_dict = load_data(filename)
    print(q1(locations, unique_char_dict))
    print(q2(locations, unique_char_dict))
