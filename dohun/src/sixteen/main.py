from src.utils import get_input_filename
from collections import Counter
import itertools
import numpy as np
import copy


STARTING_DIRECTION = np.array([0, 1])

ROTATION_MAP = {
    (0, 1): [np.array([1, 0]), np.array([-1, 0])],
    (0, -1): [np.array([1, 0]), np.array([-1, 0])],
    (1, 0): [np.array([0, -1]), np.array([0, 1])],
    (-1, 0): [np.array([0, -1]), np.array([0, 1])],
}


class Point:
    def __init__(
        self,
        coord: tuple,
        direction: np.array,
        score: int,
        cum_score: int,
        previous_point,
        path_from_previous_point: list = None,
    ):
        self.coord = coord
        self.direction = direction
        self.score = score
        self.cum_score = cum_score
        self.previous_point = previous_point
        self.path_from_previous_point = path_from_previous_point

    def describe(self):
        print("----------")
        print("coord: ", self.coord)
        print("score: ", self.score)
        print("cum_score:", self.cum_score)
        print("direction:", self.direction)
        if self.previous_point is not None:
            print("previous_point:", self.previous_point.coord)
            print("previous_point_dir:", self.previous_point.direction)
        print("----------")


class MazeMap:
    def __init__(self, maze_map: np.array):
        self.maze_map = maze_map
        self.start_and_end_set = False
        self._set_start_and_end()
        self.known_points = [[Point(self.starting_loc, STARTING_DIRECTION, 0, 0, None)]]

    def known_point_coords(self):
        return [p.coord for p_list in self.known_points for p in p_list]

    def known_points_flattened(self):
        return [p for p_list in self.known_points for p in p_list]

    def last_known_points(self):
        return self.known_points[-1]

    def last_known_point_coords(self):
        return [p.coord for p in self.known_points[-1]]

    def calculate_unknown_points(self):
        known_point_coords = self.known_point_coords()
        return list(set(self.check_points) - set(known_point_coords))

    def _set_start_and_end(self):
        temp_starting_loc = np.where(self.maze_map == 3)
        temp_ending_loc = np.where(self.maze_map == 9)

        self.starting_loc = temp_starting_loc[0][0], temp_starting_loc[1][0]
        self.ending_loc = temp_ending_loc[0][0], temp_ending_loc[1][0]
        self.start_and_end_set = True

    def display(self):
        print("-----The current food map looks like: -----")
        print(self.maze_map)
        print("\n")

    def display_new_points_on_map(self, new_point_coords: list, save=False):
        maze_map_temp = self.maze_map.copy()
        for coord in new_point_coords:
            maze_map_temp[coord] = 7
        print("-----The new points are here: -----")
        print(maze_map_temp)
        print("\n")

        if save:
            np.savetxt(f"outputs/sitspots.txt", maze_map_temp, fmt="%.0f")

    def _check_maze(self, coord: tuple):
        return self.maze_map[coord]

    def _check_surrounding_directions(self, coord: tuple, directions: list) -> list:
        possible_directions = list()
        for potential in directions:
            next_potential_coord = move_coord(coord, potential)
            if self.maze_map[next_potential_coord] == 0:
                possible_directions.append(potential)

        return possible_directions

    def find_checkpoints(self):
        all_points = np.where(self.maze_map == 0)
        check_points = [self.starting_loc, self.ending_loc]

        all_directions = list(np.array(x) for x in ROTATION_MAP.keys())
        for x_coord, y_coord in zip(all_points[0], all_points[1]):
            possible_surrounding_directions = self._check_surrounding_directions(
                (x_coord, y_coord), all_directions
            )
            if len(possible_surrounding_directions) > 2:
                check_points.append((x_coord, y_coord))
            # most points will return at least 2 because going forward and backwards
            if len(possible_surrounding_directions) == 2:
                if (
                    np.sum(
                        np.abs(
                            possible_surrounding_directions[0]
                            + possible_surrounding_directions[1]
                        )
                    )
                    != 0
                ):
                    check_points.append((x_coord, y_coord))

        self.check_points = list(set(check_points))

    def possible_ways_forward(self, coord: tuple, direction: np.array):
        potential_directions = [direction] + ROTATION_MAP[tuple(direction)]

        return self._check_surrounding_directions(coord, potential_directions)

    def _potential_connection(self, known_point: Point, coord: tuple) -> tuple:
        """
        we first check if the point is in a straight line from a coordinate. If so, we check
        that we can actually traverse in it without turning
        """
        dist_vector = (known_point.coord[0] - coord[0], known_point.coord[1] - coord[1])
        if ((dist_vector[0] != 0) or (dist_vector[1] != 0)) == 0:
            return False, None, None, None

        if not (dist_vector[0] == 0 or dist_vector[1] == 0):
            return False, None, None, None

        # direction needed to go in the direction
        abs_sum = abs(dist_vector[0] + dist_vector[1])
        assert (
            dist_vector[0] / abs_sum,
            dist_vector[1] / abs_sum,
        ) in ROTATION_MAP.keys()
        direction = np.array((dist_vector[0] / abs_sum, dist_vector[1] / abs_sum))

        # now check that there are no hindrances
        temp_checking_point = move_coord(coord, direction)
        pathway = [temp_checking_point]

        while temp_checking_point != known_point.coord:
            if self._check_maze(temp_checking_point) == 1:
                return False, None, None, None
            temp_checking_point = move_coord(temp_checking_point, direction)
            pathway.append(temp_checking_point)
        dist = 0
        if np.sum(np.abs(direction - known_point.direction)) != 0:
            dist += 1000

        return True, dist + abs_sum, direction, pathway

    def check_connected_points(
        self, coord: tuple, compare_vs_all: bool = False, check_duplicates: bool = False
    ):
        new_known_points = list()

        checks = self.last_known_points()
        if compare_vs_all:
            checks = self.known_points_flattened()

        for known_point in checks:
            connected, dist, direction, pathway = self._potential_connection(
                known_point, coord
            )
            if connected:
                new_known_point = Point(
                    coord=coord,
                    direction=direction,
                    score=dist,
                    cum_score=dist + known_point.cum_score,
                    previous_point=known_point,
                    path_from_previous_point=pathway,
                )
                new = True
                if compare_vs_all:
                    for old_point in checks:
                        if compare_two_points(new_known_point, old_point):
                            new = False
                            break

                if new:
                    new_known_points.append(new_known_point)

        return new_known_points

    def calc_final_score(self, part2: bool = False):
        potential_points = [
            p for p in self.known_points_flattened() if p.coord == self.ending_loc
        ]

        if not part2:
            return min([p.cum_score for p in potential_points])
        else:
            shortest_path_length = min([p.cum_score for p in potential_points])
            shortest_path_points = [
                p
                for p in self.known_points_flattened()
                if p.cum_score == shortest_path_length and p.coord == self.ending_loc
            ]

            sitspots = list()
            for p in shortest_path_points:
                # p.describe()
                sitspots += p.path_from_previous_point
                previous_point = p.previous_point
                while previous_point != None:
                    # previous_point.describe()
                    if previous_point.path_from_previous_point is not None:
                        sitspots += previous_point.path_from_previous_point
                    previous_point = previous_point.previous_point

            sitspots += [self.starting_loc, self.ending_loc]
            return len(set(sitspots))


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
    return MazeMap(np.array(maze_map))


def move_coord(coord: tuple, direction: np.array):
    assert len(coord) == 2
    assert len(direction) == 2

    return int(coord[0] + direction[0]), int(coord[1] + direction[1])


def compare_two_points(point1: Point, point2: Point):
    coord_check = point1.coord == point2.coord
    direction_check = np.sum(np.abs(point1.direction - point2.direction)) == 0

    if not coord_check or not direction_check:
        return False

    if point1.previous_point is None and point2.previous_point is None:
        return True

    if point1.previous_point is None or point2.previous_point is None:
        return False

    if point1.previous_point.coord == point2.previous_point.coord:
        return True
    # return compare_two_points(point1.previous_point, point2.previous_point)


def ans(
    mm: MazeMap,
) -> int:
    mm.find_checkpoints()

    unknown_coords = mm.calculate_unknown_points()
    while len(unknown_coords) > 0:
        print(len(unknown_coords))
        new_known_points = list()
        for coord in unknown_coords:
            new_known_points += mm.check_connected_points(coord, compare_vs_all=True)
        mm.known_points.append(new_known_points)
        # for new_known_point in new_known_points:
        #     new_known_point.describe()
        #     mm.display_new_points_on_map(mm.last_known_point_coords())
        unknown_coords = mm.calculate_unknown_points()

    part1_ans = mm.calc_final_score()
    print("part 1 answer is:", part1_ans)
    print("part 2 answer attempt is:", mm.calc_final_score(part2=True))


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False, is_test_test=False)
    mm = load_data(filename)
    ans(mm)
