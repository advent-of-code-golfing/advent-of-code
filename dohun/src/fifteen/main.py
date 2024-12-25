from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


str_to_direction_map: dict[str, np.array] = {
    "<": np.array([0, -1]),
    ">": np.array([0, 1]),
    "^": np.array([-1, 0]),
    "v": np.array([1, 0]),
}


class FoodMap:
    def __init__(self, food_map: np.array):
        self.food_map = food_map
        self.current_robot_location_known = False
        self.num_boxes_set = False
        self._find_current_robot_loc()
        self._set_number_of_boxes()

    def _find_current_robot_loc(self):
        assert np.sum(self.food_map == 3) == 1
        temp_current_robot_loc = np.where(self.food_map == 3)
        self.current_robot_loc = (
            temp_current_robot_loc[0][0],
            temp_current_robot_loc[1][0],
        )
        self.current_robot_location_known = True

    def _set_number_of_boxes(self):
        self.num_box_left = np.sum((self.food_map == 2))
        self.num_box_right = np.sum((self.food_map == 2))
        assert self.num_box_left == self.num_box_right
        self.num_boxes_set = True

    def _check_num_boxes(self):
        if not self.num_boxes_set:
            self._set_number_of_boxes()

        assert self.num_box_left == np.sum((self.food_map == 2))
        assert self.num_box_right == np.sum((self.food_map == 5))

    def display(self):
        print("-----The current food map looks like: -----")
        print(self.food_map)
        print("\n")

    def _move_coord(self, coord: tuple, direction: np.array):
        assert len(coord) == 2
        assert len(direction) == 2
        return coord[0] + direction[0], coord[1] + direction[1]

    def move(self, inst: str):
        direction = str_to_direction_map[inst]
        food_map = self.food_map.copy()

        new_locations = [self._move_coord(self.current_robot_loc, direction)]
        things_to_move = [3]

        while food_map[new_locations[-1]] != 0:
            if food_map[new_locations[-1]] == 1:
                return
            if food_map[new_locations[-1]] == 2 or food_map[new_locations[-1]] == 5:
                things_to_move.append(food_map[new_locations[-1]].copy())
                new_locations.append(self._move_coord(new_locations[-1], direction))

        for new_location in new_locations:
            old_location = self._move_coord(new_location, -direction)
            food_map[old_location] = 0

        for new_location, thing in zip(new_locations, things_to_move):
            food_map[new_location] = thing

        self.food_map = food_map
        self._find_current_robot_loc()

        return

    def _get_updown_coords(
        self, loc: tuple, direction: np.array, food_map: np.array
    ) -> list:
        # assert(all(direction == np.array([1, 0])) or all(direction == np.array([-1, 0])))

        new_loc = self._move_coord(loc, direction)
        new_value = food_map[new_loc]

        if new_value == 0:
            return []

        if all(direction == np.array([1, 0])) or all(direction == np.array([-1, 0])):
            if new_value == 2:
                return [new_loc, self._move_coord(new_loc, np.array([0, 1]))]

            if new_value == 5:
                return [self._move_coord(new_loc, np.array([0, -1])), new_loc]

        return [new_loc]

    def _get_updown_coords_from_list(
        self, locs: list[tuple], direction: np.array, food_map: np.array
    ) -> list:
        new_coords_to_check = list()

        for loc in locs:
            new_coords_to_check += self._get_updown_coords(loc, direction, food_map)

        return list(set(new_coords_to_check))

    def _evaluate_multiple_coords(self, coords: list, food_map: np.array) -> list:
        return [food_map[coord] for coord in coords]

    def move_part2(self, inst: str, use_old_method: bool = False, iteration=int):
        if inst in ["<", ">"] and use_old_method:
            self.move(inst)
            return

        direction = str_to_direction_map[inst]
        food_map = self.food_map.copy()

        old_locations = [[self.current_robot_loc]]
        old_values = [[3]]

        next_coords_to_check = self._get_updown_coords_from_list(
            old_locations[-1], direction, food_map
        )
        next_values_to_check = self._evaluate_multiple_coords(
            next_coords_to_check, food_map
        )

        while np.sum(next_values_to_check) != 0 or len(next_values_to_check) > 0:
            if 1 in next_values_to_check:
                return
            else:
                old_locations.append(next_coords_to_check)
                old_values.append(next_values_to_check)
                next_coords_to_check = self._get_updown_coords_from_list(
                    old_locations[-1], direction, food_map
                )
                next_values_to_check = self._evaluate_multiple_coords(
                    next_coords_to_check, food_map
                )

        for row in old_locations:
            for coord in row:
                food_map[coord] = 0

        for row, values in zip(old_locations, old_values):
            next_row = [self._move_coord(coord, direction) for coord in row]
            for coord, new_value in zip(next_row, values):
                food_map[coord] = new_value

        self.food_map = food_map
        self._find_current_robot_loc()
        self._check_num_boxes()

        return

    def calculate_location_score(self):
        box_locations = np.where(self.food_map == 2)

        score = 0
        for row_box_location, column_box_location in zip(
            box_locations[0], box_locations[1]
        ):
            score += 100 * row_box_location + column_box_location

        return score


def load_data(filename: str, part_2=False) -> list:
    food_map = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line_raw = line.strip("\n")
            line_list = []

            # If you want to replicate part i results, delete the second append line for each if statement
            for char in line_raw:
                if char == ".":
                    line_list.append(0)
                    if part_2:
                        line_list.append(0)
                elif char == "#":
                    line_list.append(1)
                    if part_2:
                        line_list.append(1)
                elif char == "O":
                    line_list.append(2)
                    if part_2:
                        line_list.append(5)
                elif char == "@":
                    line_list.append(3)
                    if part_2:
                        line_list.append(0)

            if len(line_list) > 0:
                food_map.append(line_list)

    with open(filename, "r") as f:
        instructions = f.read().strip().split("\n\n")[1]

    return FoodMap(np.array(food_map)), instructions.replace("\n", "")


def q1(fm: FoodMap, instructions: str) -> int:
    for inst in instructions:
        fm.move(inst)

    return fm.calculate_location_score()


def q2(fm: FoodMap, instructions: str) -> int:
    for i, inst in enumerate(instructions):
        # fm.display()
        fm.move_part2(inst, use_old_method=False)

    return fm.calculate_location_score()


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False, is_test_test=False)
    fm_1, instructions = load_data(filename)
    fm_2, instructions = load_data(filename, part_2=True)

    print(q1(fm_1, instructions))
    print(q2(fm_2, instructions))
