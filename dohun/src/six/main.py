from src.utils import get_input_filename
from collections import Counter

import numpy as np
import copy


def load_data(filename: str) -> tuple:
    map = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line_raw = line.strip("\n")
            line_list = []
            for char in line_raw:
                if char == ".":
                    line_list.append(0)
                elif char == "#":
                    line_list.append(1)
                else:
                    line_list.append(2)

            map.append(line_list)
        return np.array(map), "N"


ROTATION_MAP = {"N": "E", "E": "S", "S": "W", "W": "N"}


def _guard_one_iteration(
    map: np.array,
    guard_loc: tuple,
    direction: str,
    guard_tracker_map: np.array,
    with_new_route_tracking: bool = False,
) -> tuple:

    loc_i, loc_j = guard_loc
    if direction == "N":
        hurdle = map[:loc_i, loc_j]
    elif direction == "E":
        hurdle = map[loc_i, loc_j + 1 :]
    elif direction == "S":
        hurdle = map[loc_i + 1 :, loc_j]
    else:
        hurdle = map[loc_i, :loc_j]

    hurdle_exists = np.sum(hurdle == 1)

    if not hurdle_exists:
        if direction == "N":
            guard_tracker_map[:loc_i, loc_j] = 3
            if with_new_route_tracking:
                new_route = np.zeros_like(guard_tracker_map)
                new_route[:loc_i, loc_j] = 3

        elif direction == "E":
            guard_tracker_map[loc_i, loc_j + 1 :] = 3
            if with_new_route_tracking:
                new_route = np.zeros_like(guard_tracker_map)
                new_route[loc_i, loc_j + 1 :] = 3

        elif direction == "S":
            guard_tracker_map[loc_i + 1 :, loc_j] = 3
            if with_new_route_tracking:
                new_route = np.zeros_like(guard_tracker_map)
                new_route[loc_i + 1 :, loc_j] = 3

        else:
            guard_tracker_map[loc_i, :loc_j] = 3
            if with_new_route_tracking:
                new_route = np.zeros_like(guard_tracker_map)
                new_route[loc_i, :loc_j] = 3

        if with_new_route_tracking:
            return (
                map,
                ROTATION_MAP[direction],
                len(hurdle),
                guard_tracker_map,
                new_route,
            )

        return map, ROTATION_MAP[direction], len(hurdle), guard_tracker_map

    if direction == "N":
        first_hurdle = int(np.where(hurdle == 1)[0][-1])

        if first_hurdle + 1 == len(hurdle):
            map[loc_i, loc_j] = 2
            if with_new_route_tracking:
                return (
                    map,
                    ROTATION_MAP[direction],
                    0,
                    guard_tracker_map,
                    np.zeros_like(guard_tracker_map),
                )
            return map, ROTATION_MAP[direction], 0, guard_tracker_map
        hurdle_tracker = guard_tracker_map[:loc_i, loc_j]
        hurdle_tracker[first_hurdle + 1 :] = 3
        hurdle[first_hurdle + 1] = 2
        map[:loc_i, loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[first_hurdle + 1 :])
        guard_tracker_map[:loc_i, loc_j] = hurdle_tracker.copy()

        if with_new_route_tracking:
            new_route_tracker = map[:loc_i, loc_j].copy()
            new_route_tracker[first_hurdle + 1 :] = 3

            new_route = np.zeros_like(guard_tracker_map)
            new_route[:loc_i, loc_j] = new_route_tracker.copy()

            return map, "E", dist_travelled, guard_tracker_map, new_route

        return map, "E", dist_travelled, guard_tracker_map

    if direction == "E":
        first_hurdle = int(np.where(hurdle == 1)[0][0])
        if first_hurdle == 0:
            map[loc_i, loc_j] = 2
            if with_new_route_tracking:
                return (
                    map,
                    ROTATION_MAP[direction],
                    0,
                    guard_tracker_map,
                    np.zeros_like(guard_tracker_map),
                )
            return map, ROTATION_MAP[direction], 0, guard_tracker_map
        hurdle_tracker = guard_tracker_map[loc_i, loc_j + 1 :]
        hurdle_tracker[:first_hurdle] = 3
        hurdle[first_hurdle - 1] = 2
        map[loc_i, loc_j + 1 :] = hurdle.copy()
        dist_travelled = len(hurdle[:first_hurdle])
        guard_tracker_map[loc_i, loc_j + 1 :] = hurdle_tracker.copy()

        if with_new_route_tracking:
            new_route_tracker = map[loc_i, loc_j + 1 :].copy()
            new_route_tracker[:first_hurdle] = 3

            new_route = np.zeros_like(guard_tracker_map)
            new_route[loc_i, loc_j + 1 :] = new_route_tracker.copy()

            return map, "S", dist_travelled, guard_tracker_map, new_route

        return map, "S", dist_travelled, guard_tracker_map

    if direction == "S":
        first_hurdle = int(np.where(hurdle == 1)[0][0])
        if first_hurdle == 0:
            map[loc_i, loc_j] = 2
            if with_new_route_tracking:
                return (
                    map,
                    ROTATION_MAP[direction],
                    0,
                    guard_tracker_map,
                    np.zeros_like(guard_tracker_map),
                )
            return map, ROTATION_MAP[direction], 0, guard_tracker_map
        hurdle_tracker = guard_tracker_map[loc_i + 1 :, loc_j]
        hurdle_tracker[:first_hurdle] = 3
        hurdle[first_hurdle - 1] = 2
        map[loc_i + 1 :, loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[:first_hurdle])
        guard_tracker_map[loc_i + 1 :, loc_j] = hurdle_tracker.copy()

        if with_new_route_tracking:
            new_route_tracker = map[loc_i + 1 :, loc_j].copy()
            new_route_tracker[:first_hurdle] = 3

            new_route = np.zeros_like(guard_tracker_map)
            new_route[loc_i + 1 :, loc_j] = new_route_tracker.copy()

            return map, "W", dist_travelled, guard_tracker_map, new_route

        return map, "W", dist_travelled, guard_tracker_map

    if direction == "W":
        first_hurdle = int(np.where(hurdle == 1)[0][-1])
        if first_hurdle + 1 == len(hurdle):
            map[loc_i, loc_j] = 2
            if with_new_route_tracking:
                return (
                    map,
                    ROTATION_MAP[direction],
                    0,
                    guard_tracker_map,
                    np.zeros_like(guard_tracker_map),
                )
            return map, ROTATION_MAP[direction], 0, guard_tracker_map
        hurdle_tracker = guard_tracker_map[loc_i, :loc_j]
        hurdle_tracker[first_hurdle + 1 :] = 3
        hurdle[first_hurdle + 1] = 2
        map[loc_i, :loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[first_hurdle + 1 :])
        guard_tracker_map[loc_i, :loc_j] = hurdle_tracker.copy()

        if with_new_route_tracking:
            new_route_tracker = map[loc_i, :loc_j].copy()
            new_route_tracker[first_hurdle + 1 :] = 3

            new_route = np.zeros_like(guard_tracker_map)
            new_route[loc_i, :loc_j] = new_route_tracker.copy()

            return map, "N", dist_travelled, guard_tracker_map, new_route

        return map, "N", dist_travelled, guard_tracker_map


def q1(map: np.array, direction: str) -> int:
    map = map.copy()
    guard_exists = np.sum(map == 2)
    guard_tracker_map = map.copy()

    while guard_exists:
        loc_i, loc_j = (int(x) for x in np.where(map == 2))
        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3

        map, direction, dist_travelled, guard_tracker_map = _guard_one_iteration(
            map, (loc_i, loc_j), direction, guard_tracker_map
        )
        guard_exists = np.sum(map == 2)

    return np.sum(guard_tracker_map == 3)


def _check_if_loop_exists(
    previous_stops: dict,
    direction: str,
    new_route_map: np.array,
    map: np.array,
    barriers: list,
) -> list:
    # in previous_stops dict, each stopping point is mapepd with the direction it will come out of
    potential_direction = ROTATION_MAP[direction]

    potential_stops = []
    if potential_direction in previous_stops:
        potential_stops = previous_stops[potential_direction]

    if direction == "W":
        row_range, col_range = np.where(new_route_map == 3)
        row_min = row_range[0]
        row_max = row_range[-1]
        col_min = col_max = col_range[0]

        potential_col_locations = [x for x in potential_stops if x[1] < col_max]
        potential_locations = [
            x for x in potential_col_locations if x[0] >= row_min - 1 and x[1] < row_max
        ]

    if direction == "E":
        row_range, col_range = np.where(new_route_map == 3)
        row_min = row_range[0]
        row_max = row_range[-1]
        col_min = col_max = col_range[0]

        potential_col_locations = [x for x in potential_stops if x[1] > col_max]
        potential_locations = [
            x for x in potential_col_locations if x[0] > row_min and x[1] <= row_max + 1
        ]

    if direction == "N":
        row_range, col_range = np.where(new_route_map == 3)
        row_min = row_max = row_range[0]
        col_min = col_range[0]
        col_max = col_range[-1]

        potential_row_locations = [x for x in potential_stops if x[0] < row_max]
        potential_locations = [
            x for x in potential_row_locations if x[1] <= col_max + 1 and x[1] > col_min
        ]

    if direction == "S":
        row_range, col_range = np.where(new_route_map == 3)
        row_min = row_max = row_range[0]
        col_min = col_range[0]
        col_max = col_range[-1]

        potential_row_locations = [x for x in potential_stops if x[0] > row_max]
        potential_locations = [
            x for x in potential_row_locations if x[1] < col_max and x[1] >= col_min - 1
        ]

    return potential_locations


def _check_if_in_loop(map: np.array, direction: str, road_num: int = 0) -> int:
    map = map.copy()
    guard_exists = np.sum(map == 2)
    guard_tracker_map = map.copy()

    previous_stops = dict()
    while guard_exists:
        loc_i, loc_j = (int(x) for x in np.where(map == 2))
        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3
        if road_num > 0:
            if direction in previous_stops.keys():
                if (loc_i, loc_j) in previous_stops[direction]:
                    return 1
                previous_stops[direction] = previous_stops[direction] + [(loc_i, loc_j)]
            else:
                previous_stops[direction] = [(loc_i, loc_j)]

        map, direction, dist_travelled, guard_tracker_map = _guard_one_iteration(
            map, (loc_i, loc_j), direction, guard_tracker_map
        )
        guard_exists = np.sum(map == 2)
        road_num += 1

    return 0


def q2(map: np.array, direction: str) -> int:
    map = map.copy()
    guard_exists = np.sum(map == 2)
    guard_tracker_map = map.copy()

    loop_counter = 0
    poss_loop_barriers = list()
    previous_stops = dict()
    # Run once, checking every time we stop to see if we could have added a barrier
    k = 0
    barriers = [(x, y) for x, y in zip(np.where(map == 1)[0], np.where(map == 1)[1])]
    while guard_exists:
        loc_i, loc_j = (int(x) for x in np.where(map == 2))

        if k > 0:
            if direction in previous_stops.keys():
                previous_stops[direction] = previous_stops[direction] + [(loc_i, loc_j)]
            else:
                previous_stops[direction] = [(loc_i, loc_j)]

        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3

        map, direction, dist_travelled, guard_tracker_map, new_route_map = (
            _guard_one_iteration(
                map,
                (loc_i, loc_j),
                direction,
                guard_tracker_map,
                with_new_route_tracking=True,
            )
        )

        loop_loc = _check_if_loop_exists(
            previous_stops, direction, new_route_map, map, barriers
        )
        loop_counter += len(loop_loc)
        poss_loop_barriers += loop_loc
        guard_exists = np.sum(map == 2)

        k = k + 1

    return loop_counter


def brute_force_find_loops(
    old_map: np.array, new_route_map: np.array, old_direction: str, road_num: int = 0
):
    row_locs, col_locs = np.where(new_route_map == 3)
    loop_loc = []

    for row_loc, col_loc in zip(row_locs, col_locs):
        temp_map = old_map.copy()
        temp_map[row_loc, col_loc] = 1

        if _check_if_in_loop(temp_map, old_direction, 0):
            loop_loc += [(row_loc, col_loc)]

    return loop_loc


def q2_brute_force(map: np.array, direction: str):
    starting_map = map.copy()
    starting_direction = copy.copy(direction)

    map = map.copy()
    guard_exists = np.sum(map == 2)
    guard_tracker_map = map.copy()

    loop_locs = []
    road_num = 0
    while guard_exists:
        loc_i, loc_j = (int(x) for x in np.where(map == 2))
        old_map = map.copy()
        old_direction = copy.copy(direction)
        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3

        map, direction, dist_travelled, guard_tracker_map, new_route_map = (
            _guard_one_iteration(
                map,
                (loc_i, loc_j),
                direction,
                guard_tracker_map,
                with_new_route_tracking=True,
            )
        )

        new_loop_locs = brute_force_find_loops(
            old_map, new_route_map, old_direction, road_num
        )
        loop_locs += new_loop_locs
        guard_exists = np.sum(map == 2)
        road_num += 1

    unique_loop_locs = set(loop_locs)
    checking = 0
    for k in unique_loop_locs:
        temp_map = starting_map.copy()
        temp_map[k[0], k[1]] = 1
        checking += _check_if_in_loop(temp_map, starting_direction, 0)

    return len(set(loop_locs))


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False, is_test_test=False)
    map, direction = load_data(filename)
    print(q1(map, direction))
    print(q2(map, direction))
    map, direction = load_data(filename)

    print(q2_brute_force(map, direction))
