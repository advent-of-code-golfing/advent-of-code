from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy
import re
import time


def _extract_numbers_from_block(text_block: str) -> tuple:
    # Use regex to find all numbers after '+' or '='
    numbers = re.findall(r"-?\d+", text_block)
    # Flatten the list of tuples and remove None values
    extracted_numbers = [int(x) for x in numbers]

    initial_location = np.array([extracted_numbers[1], extracted_numbers[0]])
    velocity = np.array([extracted_numbers[3], extracted_numbers[2]])

    return initial_location, velocity


def load_data(filename: str) -> tuple:
    initial_locations = list()
    velocities = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            initial_location, velocity = _extract_numbers_from_block(line.strip())
            initial_locations.append(initial_location)
            velocities.append(velocity)

    if "test" in filename:
        len_rows = 7
        len_cols = 11
    else:
        len_rows = 103
        len_cols = 101

    return initial_locations, velocities, len_rows, len_cols


def _modulo_location(final_loc: tuple, len_rows: int, len_cols: int) -> tuple:
    row_loc = final_loc[0]
    col_loc = final_loc[1]

    return row_loc % len_rows, col_loc % len_cols


def q1(
    initial_locations: list,
    velocities: list,
    len_rows: int,
    len_cols: int,
    iterations: int = 100,
) -> int:
    map = np.zeros((len_rows, len_cols))

    for initial_loc, vel in zip(initial_locations, velocities):
        final_loc = initial_loc + iterations * vel
        modulo_final_loc = _modulo_location(final_loc, len_rows, len_cols)
        map[modulo_final_loc] += 1

    middle_row = int((len_rows - 1) / 2)
    middle_col = int((len_cols - 1) / 2)

    top_left_quadrant = map[:middle_row, :middle_col]
    top_right_quadrant = map[:middle_row, middle_col + 1 :]
    bottom_left_quadrant = map[middle_row + 1 :, :middle_col]
    bottom_right_quadrant = map[middle_row + 1 :, middle_col + 1 :]

    product = 1
    for quadrant in [
        top_left_quadrant,
        top_right_quadrant,
        bottom_left_quadrant,
        bottom_right_quadrant,
    ]:
        product *= np.sum(quadrant)

    return int(product)


def _check_map_for_mostly_in_one_quadrant(map: np.array, len_rows: int, len_cols: int):
    middle_row = int((len_rows - 1) / 2)
    middle_col = int((len_cols - 1) / 2)

    top_left_quadrant = map[:middle_row, :middle_col]
    top_right_quadrant = map[:middle_row, middle_col + 1 :]
    bottom_left_quadrant = map[middle_row + 1 :, :middle_col]
    bottom_right_quadrant = map[middle_row + 1 :, middle_col + 1 :]

    max_perc = 0
    map_sum = np.sum(map)
    for quadrant in [
        top_left_quadrant,
        top_right_quadrant,
        bottom_left_quadrant,
        bottom_right_quadrant,
    ]:
        max_perc = max(max_perc, np.sum(quadrant) / np.sum(map))

    return max_perc


def q2(initial_locations: list, velocities: list, len_rows: int, len_cols: int) -> int:
    max_densities = dict()
    for i in range(10000):
        map = np.zeros((len_rows, len_cols))
        for initial_loc, vel in zip(initial_locations, velocities):
            final_loc = initial_loc + i * vel
            modulo_final_loc = _modulo_location(final_loc, len_rows, len_cols)
            map[modulo_final_loc] += 1

        max_densities[i] = _check_map_for_mostly_in_one_quadrant(
            map, len_rows, len_cols
        )
        if max_densities[i] > 0.5:
            print(max_densities[i])
            np.savetxt(f"outputs/quadrant_check/{i}_iteration.txt", map, fmt="%.0f")


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    initial_locations, velocities, len_rows, len_cols = load_data(filename)
    print(q1(initial_locations, velocities, len_rows, len_cols))
    t0 = time.time()
    print(q2(initial_locations, velocities, len_rows, len_cols))
    t1 = time.time()

    print(f"Takes {t1-t0} seconds")
