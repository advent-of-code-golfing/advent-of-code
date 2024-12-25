from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


DIRECTIONS = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]


class ComputerMaze:
    def __init__(
        self,
        maze: np.array,
    ):
        self.maze = maze
        self._set_start_and_end_loc()
        self.initialize_cheat_trackers()

    def initialize_cheat_trackers(self):
        self.path_to_dist_dict = dict()
        self.cheat_available = dict()

    def _set_start_and_end_loc(self):
        self.num_rows = len(self.maze)
        self.num_cols = len(self.maze)
        self.start_loc = np.where(self.maze == 3)[0][0], np.where(self.maze == 3)[1][0]
        self.end_loc = np.where(self.maze == 9)[0][0], np.where(self.maze == 9)[1][0]

    def _in_range(self, coord: tuple):
        row_loc = coord[0]
        col_loc = coord[1]
        len_row = self.num_rows
        len_col = self.num_cols

        row_in_range = row_loc >= 0 and row_loc < len_row
        col_in_range = col_loc >= 0 and col_loc < len_row

        return row_in_range and col_in_range

    def _move(self, coord: tuple, direction: np.array):
        return coord[0] + direction[0], coord[1] + direction[1]

    def display_maze(self, num_steps: int = 0):
        new_maze = self.maze
        print("-------------")
        print(new_maze)
        print("-------------")

    def display_current_checked_points(self, coords: list):
        temp_maze = copy.deepcopy(self.maze)
        for coord in coords:
            temp_maze[coord] = 5

        print("-------------")
        print(temp_maze)
        print("-------------")

    def _find_neighbors(self, coord: tuple) -> list:
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

    def check_for_cheats(
        self,
        coord: tuple,
        maze: np.array,
        known_coords: list,
        starting_path_length: int,
    ):
        for direction in DIRECTIONS:
            one_point_out = self._move(coord, direction)
            two_point_out = self._move(one_point_out, direction)

            if not self._in_range(two_point_out):
                continue

            if not (maze[one_point_out] == 1 and maze[two_point_out] == 0) and not (
                maze[one_point_out] == 1 and maze[two_point_out] == 9
            ):
                continue

            if two_point_out in known_coords:
                continue

            if two_point_out in self.cheat_available:
                self.cheat_available[two_point_out].append(starting_path_length + 2)
            else:
                self.cheat_available[two_point_out] = [starting_path_length + 2]

    def check_for_cheats_multi_len(
        self,
        coord: tuple,
        maze: np.array,
        known_coords_dict: dict,
        starting_path_length: int,
        cheat_len: int = 20,
        part_1=True,
    ):
        if coord == (1, 1):
            print("hello")
        known_points = old_points = [coord]
        new_cheats = []
        for dist in range(1, cheat_len + 1):
            new_points = []
            if dist == 1 and part_1:
                neighbors = self._find_neighbors(coord)
                for neighbor in neighbors:
                    if maze[neighbor] == 1:
                        new_points.append(neighbor)
                known_points += new_points
                old_points = new_points
            else:
                new_new_cheats = list()
                all_neighbors = list()
                for point in old_points:
                    all_neighbors += self._find_neighbors(point)
                all_neighbors = list(set(all_neighbors))
                for neighbor in all_neighbors:
                    if neighbor not in known_points and neighbor not in new_points:
                        new_points.append(neighbor)
                    if maze[neighbor] == 0 or maze[neighbor] == 9:
                        if neighbor in known_coords_dict.keys():
                            continue
                        if neighbor not in new_cheats:
                            new_cheats.append(neighbor)
                            if neighbor in self.cheat_available:
                                self.cheat_available[neighbor].append(
                                    (starting_path_length + dist, coord)
                                )
                            else:
                                self.cheat_available[neighbor] = [
                                    (starting_path_length + dist, coord)
                                ]

                if len(new_points) == 0:
                    break
                known_points += new_points
                old_points = new_points

    def find_shortest_path(
        self,
        start_loc: tuple = None,
        num_cheats: int = 0,
        starting_path_length: int = 0,
        cheat_len: int = 2,
        part_1: bool = True,
    ) -> tuple:
        if start_loc is None:
            start_loc = self.start_loc

        old_known_coords = [start_loc]
        known_coords_dict = {start_loc: True}
        maze = copy.deepcopy(self.maze)
        path_length = starting_path_length
        while self.end_loc not in old_known_coords:
            new_known_coords = list()
            all_neighbors = list()
            for coord in old_known_coords:
                if num_cheats > 0:
                    self.check_for_cheats_multi_len(
                        coord=coord,
                        maze=maze,
                        known_coords_dict=known_coords_dict,
                        starting_path_length=path_length,
                        cheat_len=cheat_len,
                        part_1=part_1,
                    )
                all_neighbors += self._find_neighbors(coord)
            all_neighbors = list(set(all_neighbors))
            for neighbor in all_neighbors:
                if maze[neighbor] == 1:
                    continue
                if neighbor in known_coords_dict.keys():
                    continue
                if neighbor not in new_known_coords:
                    new_known_coords.append(neighbor)
            assert len(new_known_coords) == 1
            for new_known_coord in new_known_coords:
                known_coords_dict[new_known_coord] = True
            path_length += 1
            self.path_to_dist_dict[new_known_coords[0]] = path_length

            if len(new_known_coords) == 0:
                return False, path_length

            old_known_coords = new_known_coords

        return True, path_length


def load_data(filename: str) -> list:
    maze_map = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line_raw = line.strip("\n")
            line_list = []

            for char in line_raw:
                if char == ".":
                    line_list.append(0)
                elif char == "#":
                    line_list.append(1)
                elif char == "E":
                    line_list.append(9)
                elif char == "S":
                    line_list.append(3)

            maze_map.append(line_list)
    return ComputerMaze(np.array(maze_map))


def q1(cm: ComputerMaze) -> int:
    _, shortest_path = cm.find_shortest_path(num_cheats=1, starting_path_length=0)

    savings_dict = dict()
    path_dict = cm.path_to_dist_dict
    saves_100 = 0
    for end_coord, dist_array in cm.cheat_available.items():
        for data in dist_array:
            dist, start_coord = data
            dist_to_finish = path_dict[end_coord] - dist

            if dist_to_finish >= 100:
                saves_100 += 1
            if dist_to_finish in savings_dict:
                savings_dict[dist_to_finish] += 1
            else:
                savings_dict[dist_to_finish] = 1
    return saves_100


def q2(cm: ComputerMaze) -> int:
    cm.initialize_cheat_trackers()
    _, shortest_path = cm.find_shortest_path(
        num_cheats=1, starting_path_length=0, cheat_len=20, part_1=False
    )

    savings_dict = dict()
    savings_dict_coords = dict()
    path_dict = cm.path_to_dist_dict
    saves_100 = 0
    for end_coord, dist_array in cm.cheat_available.items():
        for data in dist_array:
            dist, start_coord = data
            dist_to_finish = path_dict[end_coord] - dist
            if dist_to_finish >= 100:
                saves_100 += 1
            if dist_to_finish > 0:
                if dist_to_finish in savings_dict:
                    savings_dict[dist_to_finish] += 1
                    savings_dict_coords[dist_to_finish].append((start_coord, end_coord))
                else:
                    savings_dict[dist_to_finish] = 1
                    savings_dict_coords[dist_to_finish] = [(start_coord, end_coord)]

    coord_to_check = savings_dict_coords[64]
    temp_dict = dict()
    for s in coord_to_check:
        if s in temp_dict:
            temp_dict[s] += 1
        else:
            temp_dict[s] = 1
    return saves_100


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    cm = load_data(filename)
    print(q1(cm))
    print(q2(cm))
