from collections import deque, defaultdict
from copy import deepcopy
from typing import Any

from src.common import Vector, Map, DIRECTIONS
from src.utils import get_input_filename
from bisect import bisect_right


class TrackVector(Vector):
    def __init__(self, row: int, col: int) -> None:
        self.distance_to_end = -1
        return super().__init__(row, col)


class RaceTrack(Map):
    def __init__(
        self, map: list[list[Any]], start: TrackVector, end: TrackVector
    ) -> None:
        self.start = start
        self.end = end
        super().__init__(map)
        self.default_distance = 0
        self.generate_shortest_paths()
        self.results: defaultdict[int, int] = defaultdict(int)

    def generate_cheat_paths(self, max_cheat: int) -> dict[int, int]:
        start = self.start
        steps = 0
        queue: deque[TrackVector] = deque()
        queue.append(start)
        been: set[Vector] = set()

        while queue:
            current_level = len(queue)
            # print(path_len, queue)
            for _ in range(current_level):
                cur = queue.popleft()
                been.add(cur)
                self.find_cheat_paths(cur, steps, max_cheat)
                if cur == self.end:
                    return self.results
                for dir in DIRECTIONS:
                    next_point = cur + dir
                    next_point = TrackVector(next_point.row, next_point.col)
                    if next_point in been or next_point in queue:
                        continue
                    if not self.within_range(next_point):
                        continue
                    if self.get_val(next_point) == "#":
                        continue
                    queue.append(next_point)

            steps += 1
        raise RuntimeError

    def find_cheat_paths(self, cur: TrackVector, steps: int, max_cheat: int) -> None:
        potential_cheat_ends = [
            vec for vec in self.distances_to_end if cur.distance(vec) <= max_cheat
        ]

        for pot_end in potential_cheat_ends:
            total_distance_to_end = (
                steps + cur.distance(pot_end) + pot_end.distance_to_end
            )
            diff = self.default_distance - total_distance_to_end
            if diff > 0:
                self.results[diff] += 1

    def generate_shortest_paths(self) -> None:
        """
        Generates the shortest path from each point in the track to the end point
        """
        self.distances_to_end: list[TrackVector] = []
        # We start from the end point, and navigate through the maze backwards.
        # The number of steps from the end will naturally be the shortest path back

        queue: deque[TrackVector] = deque()
        queue.append(self.end)
        been: set[TrackVector] = set()

        num_steps = 0

        while queue:
            current_level = len(queue)
            for _ in range(current_level):
                cur = queue.popleft()
                cur.distance_to_end = num_steps
                if cur == self.start:
                    self.default_distance = num_steps
                self.distances_to_end.append(cur)
                been.add(cur)
                for dir in DIRECTIONS:
                    next_point = TrackVector(cur.row + dir.row, cur.col + dir.col)
                    if next_point in been or next_point in queue:
                        continue
                    if not self.within_range(next_point):
                        continue
                    if self.get_val(next_point) == "#":
                        continue
                    queue.append(next_point)
            num_steps += 1

        self.distances_to_end.sort(key=lambda x: x.distance_to_end)


def load_data(filename: str) -> RaceTrack:
    track: list[list[str]] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            track.append([*line.strip()])

    start, end = None, None

    for row in range(len(track)):
        for col in range(len(track[0])):
            if track[row][col] == "S":
                start = TrackVector(row, col)
                track[row][col] = "."
            elif track[row][col] == "E":
                end = TrackVector(row, col)
                track[row][col] = "."

    if start is None or end is None:
        raise ValueError

    res = RaceTrack(track, start, end)
    return res


def solve_part_one(track: RaceTrack) -> int:
    # This is same as saying we can change a wall "#" to a path "."
    # for dist in track.distances_to_end:
    #     print(dist, dist.distance_to_end)
    res = track.generate_cheat_paths(2)
    total = 0

    for time_saved, count in res.items():
        if time_saved >= 100:
            total += count

    return total


def solve_part_two(track: RaceTrack) -> int:
    res = track.generate_cheat_paths(20)
    total = 0

    for time_saved, count in res.items():
        if time_saved >= 100:
            total += count
    return total


def run(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)

    if test:
        print(solve_part_one(deepcopy(data)))
        print(solve_part_two(deepcopy(data)))
    else:
        print(solve_part_one(deepcopy(data)))
        print(solve_part_two(deepcopy(data)))


if __name__ == "__main__":
    run(False)
