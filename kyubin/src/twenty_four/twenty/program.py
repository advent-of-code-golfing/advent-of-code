from collections import deque, defaultdict
from copy import deepcopy
from typing import Any

from src.common import Vector, Map, DIRECTIONS
from src.utils import get_input_filename


class TrackVector(Vector):
    def __init__(self, row: int, col: int) -> None:
        self.cheat_used = False
        return super().__init__(row, col)


class RaceTrack(Map):
    def __init__(
        self, map: list[list[Any]], start: TrackVector, end: TrackVector
    ) -> None:
        self.start = start
        self.end = end
        super().__init__(map)

    def get_shortest_path(self) -> int:
        path_len = 1
        queue: deque[TrackVector] = deque()
        queue.append(self.start)
        been: set[Vector] = set()

        while queue:
            current_level = len(queue)
            # print(path_len, queue)
            for _ in range(current_level):
                cur = queue.popleft()
                been.add(cur)
                if cur == self.end:
                    return path_len - 1
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

            path_len += 1
        raise RuntimeError


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
    counts: dict[int, int] = defaultdict(int)
    orig_time = track.get_shortest_path()

    for row in range(track.nrows):
        print(row)
        for col in range(track.ncols):
            if track.get_val(Vector(row, col)) != "#":
                continue
            new_track = deepcopy(track)
            # Make the wall a track
            new_track.map[row][col] = "."
            new_time = new_track.get_shortest_path()
            diff = orig_time - new_time
            counts[diff] += 1

    total = 0
    for k, v in counts.items():
        if k >= 100:
            total += v

    return total


def solve_part_two(track: RaceTrack) -> int:
    return 0


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
