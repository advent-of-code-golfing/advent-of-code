from src.utils import get_input_filename
from collections import defaultdict
import itertools

import numpy as np
import copy


def load_data(filename: str) -> list:
    top_map = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            nums = line.strip("\n")
            top_map.append([int(l) for l in nums])

    return np.array(top_map)


def _neighboring_coords(row_loc: int, col_loc: int, len_row: int, len_col: int) -> list:
    if row_loc < 0 or row_loc >= len_row:
        raise ValueError(f"row {row_loc} coordinate out of range in neighbor search")
    if col_loc < 0 or col_loc >= len_col:
        raise ValueError(f"col {col_loc} coordinate out of range in neighbor search")

    poss_row_locs = [row_loc - 1, row_loc + 1]
    if row_loc == 0:
        poss_row_locs = [row_loc + 1]
    elif row_loc == len_row - 1:
        poss_row_locs = [row_loc - 1]

    poss_col_locs = [col_loc - 1, col_loc + 1]
    if col_loc == 0:
        poss_col_locs = [col_loc + 1]
    elif col_loc == len_col - 1:
        poss_col_locs = [col_loc - 1]

    possible_coords = []
    for poss_row_loc in poss_row_locs:
        possible_coords.append((poss_row_loc, col_loc))

    for poss_col_loc in poss_col_locs:
        possible_coords.append((row_loc, poss_col_loc))

    return possible_coords


def _create_location_map(last_location: list):
    location_to_index = dict()
    for i, coord in enumerate(last_location):
        if coord in location_to_index:
            location_to_index[coord] = location_to_index[coord] + [i]
        else:
            location_to_index[coord] = [i]

    return location_to_index


def q1(top_map: list) -> int:
    num_rows = len(top_map)
    num_cols = len(top_map[0])

    t_h = np.where(top_map == 0)
    potential_paths = dict()
    potential_paths[0] = list()
    for row_loc, col_loc in zip(t_h[0], t_h[1]):
        potential_paths[0].append([(row_loc, col_loc)])

    for i in range(1, 10):
        last_location = [x[-1] for x in potential_paths[i - 1]]
        location_to_index = _create_location_map(last_location)

        new_potential_paths = list()
        for coord, indices in location_to_index.items():
            neighbors = _neighboring_coords(coord[0], coord[1], num_rows, num_cols)

            for neighbor in neighbors:
                if top_map[neighbor] == i:
                    for index in indices:
                        new_temp_list = potential_paths[i - 1][index] + [neighbor]
                        new_potential_paths.append(new_temp_list)

        potential_paths[i] = new_potential_paths

    score_dict = dict()
    for initial_path in potential_paths[0]:
        starting_point = initial_path[0]
        paths_filtered = [x[-1] for x in potential_paths[9] if x[0] == starting_point]
        score_dict[starting_point] = list(set(paths_filtered))

    return sum([len(x) for x in score_dict.values()])


def q2(top_map: list) -> int:
    num_rows = len(top_map)
    num_cols = len(top_map[0])

    t_h = np.where(top_map == 0)
    potential_paths = dict()
    potential_paths[0] = list()
    for row_loc, col_loc in zip(t_h[0], t_h[1]):
        potential_paths[0].append([(row_loc, col_loc)])

    for i in range(1, 10):
        last_location = [x[-1] for x in potential_paths[i - 1]]
        location_to_index = _create_location_map(last_location)

        new_potential_paths = list()
        for coord, indices in location_to_index.items():
            neighbors = _neighboring_coords(coord[0], coord[1], num_rows, num_cols)

            for neighbor in neighbors:
                if top_map[neighbor] == i:
                    for index in indices:
                        new_temp_list = potential_paths[i - 1][index] + [neighbor]
                        new_potential_paths.append(new_temp_list)

        potential_paths[i] = new_potential_paths

    return len(potential_paths[9])


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    top_map = load_data(filename)
    print(q1(top_map))
    print(q2(top_map))
