from collections import deque
from copy import deepcopy
from typing import Any

from src.common import Vector, Map, DIRECTIONS
from src.utils import get_input_filename


class ByteMap(Map):
    def __init__(self, map: list[list[Any]], bytes: list[Vector]) -> None:
        super().__init__(map)
        self.bytes = bytes

    def add_first_n_bytes(self, n: int) -> None:
        for i in range(n):
            cur = self.bytes[i]
            self.add_byte(cur)

    def add_byte(self, vec: Vector) -> None:
        self.map[vec.row][vec.col] = "#"


def load_data(filename: str, size: int) -> ByteMap:
    grid = [["." for _ in range(size)] for _ in range(size)]
    incoming_bytes: list[Vector] = []

    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            col, row = [int(val) for val in line.split(",")]
            incoming_bytes.append(Vector(row, col))

    map = ByteMap(grid, incoming_bytes)
    return map


def solve_part_one(map: ByteMap, n_fallen: int) -> int:
    start = Vector(0, 0)
    n = len(map.map) - 1
    end = Vector(n, n)
    map.add_first_n_bytes(n_fallen)

    path_len = 1
    queue: deque[Vector] = deque()
    queue.append(start)
    been: set[Vector] = set()

    while queue:
        current_level = len(queue)
        # print(path_len, queue)
        for _ in range(current_level):
            cur = queue.popleft()
            been.add(cur)
            if cur == end:
                return path_len - 1
            for dir in DIRECTIONS:
                next_point = cur + dir
                if next_point in been or next_point in queue:
                    continue
                if not map.within_range(next_point):
                    continue
                if map.get_val(next_point) == "#":
                    continue
                queue.append(next_point)

        path_len += 1
    raise RuntimeError


def solve_part_two(map: ByteMap) -> str:
    for i in range(len(map.bytes)):
        try:
            solve_part_one(map, i)
        except RuntimeError:
            treshold_byte = map.bytes[i - 1]
            return f"{treshold_byte.col},{treshold_byte.row}"
    return ""


def run(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    if test:
        grid_size = 7
        num_bytes = 12
    else:
        grid_size = 71
        num_bytes = 1024

    data = load_data(filename, grid_size)

    if test:
        print(solve_part_one(deepcopy(data), num_bytes))
        print(solve_part_two(deepcopy(data)))
    else:
        print(solve_part_one(deepcopy(data), num_bytes))
        print(solve_part_two(deepcopy(data)))


if __name__ == "__main__":
    run(False)
