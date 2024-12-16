from collections import deque

from src.common import Vector, Map
from src.utils import get_input_filename

from typing import Any


class TrailMap(Map):
    def __init__(self, map: list[list[Any]], starting_points: list[Vector]):
        self.starting_points = starting_points
        return super().__init__(map)


def load_data(filename: str) -> TrailMap:
    map: list[list[int]] = []
    starting_points: list[Vector] = []

    with open(filename, "r") as f:
        for row, line in enumerate(f.readlines()):
            cur_row: list[int] = []
            for col, val in enumerate(line.strip()):
                cur_row.append(int(val))
                if int(val) == 0:
                    starting_points.append(Vector(row, col))
            map.append(cur_row)

    trail_map = TrailMap(map, starting_points)
    return trail_map


def dfs(map: TrailMap, start: Vector, part: int) -> int:

    dirs = [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]

    nines_been: list[Vector] = []
    total_nines = 0
    q: deque[Vector] = deque()
    q.append(start)

    while q:
        cur = q.popleft()
        cur_val = map.get_val(cur)
        # Add to solutions if we reach a 9
        # Part 1 for unique 9s part 2 for all 9s
        if cur_val == 9:
            total_nines += 1
            if cur not in nines_been:
                nines_been.append(cur)
        # Check each direction from current point
        for dir in dirs:
            next_point: Vector = cur + dir
            # Skip if this point is outside of the range of the map
            if not map.within_range(next_point):
                continue
            next_val = map.get_val(next_point)

            # Add to queue if this is a potential next step in the trail
            if next_val == cur_val + 1:
                q.append(next_point)

    if part == 1:
        return len(nines_been)
    else:
        return total_nines


def solve_part_one(map: TrailMap) -> int:

    total = 0
    for start in map.starting_points:
        total += dfs(map, start, 1)
    return total


def solve_part_two(map: TrailMap) -> int:

    total = 0
    for start in map.starting_points:
        total += dfs(map, start, 2)
    return total


if __name__ == "__main__":
    filename = get_input_filename(__file__, True)
    map = load_data(filename)
    print(solve_part_one(map))
    print(solve_part_two(map))
