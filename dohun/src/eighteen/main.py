from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy
import time


POSSIBLE_DIRECTIONS = [
    np.array([1, 0]),
    np.array([-1, 0]),
    np.array([0, 1]),
    np.array([0, -1]),
]


def _initialize_maze(num_rows: int, num_cols: int) -> np.array:
    return np.zeros((num_rows, num_cols))


class ComputerMaze:
    def __init__(self, empty_maze: np.array, corrupt_coords: list[tuple[int, int]]):
        self.empty_maze = empty_maze
        self.corrupt_coords = corrupt_coords
        self.current_state_initialized = False
        self._set_start_and_end_loc()

    def _set_start_and_end_loc(self):
        self.num_rows = len(self.empty_maze)
        self.num_cols = len(self.empty_maze)
        self.start_loc = (0, 0)
        self.end_loc = (self.num_rows - 1, self.num_cols - 1)

    def _maze_after_n_steps(self, num_steps: int):
        new_maze = _initialize_maze(len(self.empty_maze), len(self.empty_maze[0]))

        for i in range(num_steps):
            new_maze[self.corrupt_coords[i]] = 1

        return new_maze

    def display_maze(self, num_steps: int = 0):
        new_maze = self._maze_after_n_steps(num_steps)
        print("-------------")
        print(new_maze)
        print("-------------")

    def _initialize_current_maze_state(self, num_steps: int = 0):
        self.current_maze = self._maze_after_n_steps(num_steps)
        self.current_state_initialized = True

    def _find_neighbors(self, coord: tuple):
        row_loc = coord[0]
        col_loc = coord[1]
        len_row = self.num_rows
        len_col = self.num_cols

        if row_loc < 0 or row_loc >= len_row:
            raise ValueError(
                f"row {row_loc} coordinate out of range in neighbor search"
            )
        if col_loc < 0 or col_loc >= len_col:
            raise ValueError(
                f"col {col_loc} coordinate out of range in neighbor search"
            )

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

    def display_current_checked_points(self, save: bool = False):
        temp_maze = self.current_maze
        for coord in self.known_coords:
            temp_maze[coord] = 5

        print("-------------")
        print(temp_maze)
        print("-------------")

        if save:
            np.savetxt(
                f"outputs/eighteen_maze/current_search_{len(self.known_coords)}.txt",
                temp_maze,
                fmt="%.0f",
            )

    def find_shortest_path(self, num_steps: int) -> tuple:
        if not self.current_state_initialized:
            self._initialize_current_maze_state(num_steps)

        self.known_coords = old_known_coords = [self.start_loc]
        path_length = 0
        while self.end_loc not in old_known_coords:
            new_known_coords = list()
            all_neighbors = list()
            for coord in old_known_coords:
                all_neighbors += self._find_neighbors(coord)
            all_neighbors = list(set(all_neighbors))
            for neighbor in all_neighbors:
                if self.current_maze[neighbor] == 1:
                    continue
                if neighbor in self.known_coords:
                    continue
                new_known_coords.append(neighbor)
            path_length += 1
            self.known_coords += new_known_coords
            # self.display_current_checked_points()
            if len(new_known_coords) == 0:
                return False, path_length

            old_known_coords = new_known_coords

            # Initialize maze again for future runs
            self.current_state_initialized = False
        return True, path_length


def load_data(filename: str) -> list:
    zero_maze = _initialize_maze(71, 71)
    if "test" in filename:
        zero_maze = _initialize_maze(7, 7)

    corrupt_coords = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue
            corrupt_coord = tuple(int(x) for x in line.strip().split(","))
            corrupt_coord = corrupt_coord[1], corrupt_coord[0]
            corrupt_coords.append(corrupt_coord)

    return ComputerMaze(zero_maze, corrupt_coords)


def q1(
    cm: ComputerMaze,
) -> int:
    return cm.find_shortest_path(1024)[1]


def q2(
    cm: ComputerMaze,
) -> int:
    path_exists, path_len = cm.find_shortest_path(1024)
    num_coords = len(cm.corrupt_coords)
    for i in range(1024 + 1, num_coords):
        path_exists, path_len = cm.find_shortest_path(i)
        if not path_exists:
            return cm.corrupt_coords[i - 1][1], cm.corrupt_coords[i - 1][0]

        if i % 10 == 0:
            print(i)

    return 0


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    cm = load_data(filename)
    print(q1(cm))
    print(q2(cm))
