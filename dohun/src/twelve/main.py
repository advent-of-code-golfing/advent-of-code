from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str) -> list:
    all_strs = ""
    locations = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            all_strs += line.strip("\n")
        unique_chars = set(all_strs)
        unique_char_dict = dict(zip(unique_chars, range(1, len(unique_chars) + 1)))

    with open(filename, "r") as f:
        for line in f.readlines():
            locations.append([unique_char_dict[x] for x in line.strip("\n")])

    return np.array(locations), unique_char_dict


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


def _get_perimeter_and_area_from_coords(
    region: list, farm_map_original: np.array, crop: int
):
    area = len(region)

    perimeter = 0
    for point in region:
        neighbors = _neighboring_coords(
            point[0], point[1], len(farm_map_original), len(farm_map_original)
        )

        actual_neighbors = []
        for neighbor in neighbors:
            if farm_map_original[neighbor] != crop:
                actual_neighbors.append(neighbor)
        farm_border = 4 - len(neighbors)
        perimeter += len(actual_neighbors) + farm_border

    return area, perimeter


def _get_regions(farm_map: np.array, mapping: dict) -> dict:
    len_rows = len(farm_map)
    len_cols = len(farm_map[0])
    regions = dict()

    # First split the map into regions
    for crop in mapping.values():
        while np.sum(farm_map == crop) != 0:
            crop_locations = np.where(farm_map == crop)
            starting_loc = crop_locations[0][0], crop_locations[1][0]

            current_region = boundaries = [starting_loc]
            while len(boundaries) > 0:
                new_boundaries = list()
                for boundary in boundaries:
                    temp = _neighboring_coords(
                        boundary[0], boundary[1], len_rows, len_cols
                    )
                    for new_point in temp:
                        if farm_map[new_point] == crop:
                            new_boundaries.append(new_point)

                new_boundaries = list(set(new_boundaries))
                boundaries = list(set(new_boundaries) - set(current_region))
                current_region = list(set(current_region + new_boundaries))

            if crop in regions:
                regions[crop] += [current_region]
            else:
                regions[crop] = [current_region]

            for i in current_region:
                farm_map[i] = 0

    return regions


def q1(farm_map: np.array, mapping: dict) -> int:
    regions = _get_regions(farm_map.copy(), mapping)

    reverse_mapping = {v: k for k, v in mapping.items()}
    fence_price = 0
    for crop in regions:
        for region in regions[crop]:
            print("for crop", reverse_mapping[crop])
            area, perimeter = _get_perimeter_and_area_from_coords(
                region,
                farm_map,
                crop,
            )
            print("area", "perimeter", area, perimeter)
            print("so price", area * perimeter)
            print("\n")
            fence_price += area * perimeter

    return fence_price


def _extended_neighboring_coords(row_loc: int, col_loc: int) -> tuple:
    """
    returns neighbors in order
    1 2 3
    4   5
    6 7 8
    """
    c_1 = row_loc - 1, col_loc - 1
    c_2 = row_loc - 1, col_loc
    c_3 = row_loc - 1, col_loc + 1
    c_4 = row_loc, col_loc - 1
    c_5 = row_loc, col_loc + 1
    c_6 = row_loc + 1, col_loc - 1
    c_7 = row_loc + 1, col_loc
    c_8 = row_loc + 1, col_loc + 1

    return c_1, c_2, c_3, c_4, c_5, c_6, c_7, c_8


def _check_if_new(new_right_angle: tuple, right_angles: list) -> list:
    if new_right_angle not in right_angles:
        right_angles.append(new_right_angle)

    return right_angles


def _count_right_angles(region, farm_map, crop):
    right_angles = []
    for point in region:
        c_1, c_2, c_3, c_4, c_5, c_6, c_7, c_8 = _extended_neighboring_coords(
            point[0], point[1]
        )
        """
        if we have a map like 
        1 2 3 
        4   5
        6 7 8 
        The possible right angles are: 
        1) 2, 4 not in the region 
        2) 2, 4 in region, 1 not in region 
        3) 2, 5 not in region 
        4) 2, 5 in region, 3 not in region 
        5) 4, 7 not in regino
        6) 4, 7 in region, 6 not in region 
        7) 5, 7 not in region 
        8) 5, 7 in region, 8 not in region 
        Some of these are obvious mutually exclusive (There's more actually, is it enough to check these? maybe)
        """
        if c_2 not in region and c_4 not in region:
            """
            for convention, let's use right -> left, top -> bottom, to avoid double counting
            """
            new_right_angle = c_4, c_2, point
            right_angles = _check_if_new(new_right_angle, right_angles)
        elif c_2 in region and c_4 in region and c_1 not in region:
            new_right_angle = c_4, c_2, point
            right_angles = _check_if_new(new_right_angle, right_angles)

        if c_2 not in region and c_5 not in region:
            new_right_angle = c_2, point, c_5
            right_angles = _check_if_new(new_right_angle, right_angles)
        elif c_2 in region and c_5 in region and c_3 not in region:
            new_right_angle = c_2, point, c_5
            right_angles = _check_if_new(new_right_angle, right_angles)

        if c_4 not in region and c_7 not in region:
            new_right_angle = c_4, point, c_7
            right_angles = _check_if_new(new_right_angle, right_angles)
        elif c_4 in region and c_7 in region and c_6 not in region:
            new_right_angle = c_4, point, c_7
            right_angles = _check_if_new(new_right_angle, right_angles)

        if c_5 not in region and c_7 not in region:
            new_right_angle = point, c_7, c_5
            right_angles = _check_if_new(new_right_angle, right_angles)
        elif c_5 in region and c_7 in region and c_8 not in region:
            new_right_angle = point, c_7, c_5
            right_angles = _check_if_new(new_right_angle, right_angles)

    return len(right_angles)


def q2(stones_list: list, iterations: int = 75) -> int:
    regions = _get_regions(farm_map.copy(), mapping)

    fence_price = 0
    for crop in regions:
        for region in regions[crop]:
            right_angles = _count_right_angles(region, farm_map, crop)
            area = len(region)
            fence_price += area * right_angles
    return fence_price


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False, is_test_test=False)
    farm_map, mapping = load_data(filename)
    print(q1(farm_map, mapping))
    print(q2(farm_map, mapping))
