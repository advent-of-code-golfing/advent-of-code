from collections import deque, defaultdict
from copy import deepcopy
from typing import Any

from src.common import Map, Vector
from src.utils import get_input_filename

DIRS = [Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1)]
FENCE_DIRS = ["D", "U", "R", "L"]


class PlantPos(Vector): ...


class Fence(Vector):
    def __init__(self, row: int, col: int, dir: str) -> None:
        self.dir = dir
        return super().__init__(row, col)


class Farm(Map):
    def __init__(self, map: list[list[Any]]) -> None:
        self.regions: list["Region"] = []
        super().__init__(map)

    def get_next_val(self, pos: PlantPos) -> PlantPos:
        next_col = pos.col + 1
        if next_col == self.ncols:
            return PlantPos(pos.row + 1, 0)
        return PlantPos(pos.row, next_col)

    def get_cost(self) -> int:
        cost = 0
        for region in self.regions:
            cost += region.get_area() * region.get_perimeter()
        return cost

    def get_cost_part_two(self) -> int:
        cost = 0
        for region in self.regions:
            cost += region.get_area() * region.get_perimeter_part_two()
        return cost


class Region:
    def __init__(self, region: list[PlantPos], val: str) -> None:
        self.region = region
        self.val = val

    def __str__(self) -> str:
        return f"Size: {len(self.region)}, Val: {self.val}, Perim 1: {self.get_perimeter()}, Perim 2: {self.get_perimeter_part_two()}"

    def get_area(self) -> int:
        return len(self.region)

    def get_perimeter(self) -> int:
        # Border positions
        borders: set[PlantPos] = set()

        for pos in self.region:
            for dir in DIRS:
                border_pos = PlantPos(pos.row * 2 + dir.row, pos.col * 2 + dir.col)
                if border_pos in borders:
                    borders.remove(border_pos)
                else:
                    borders.add(border_pos)
        return len(borders)

    def get_perimeter_part_two(self) -> int:
        borders: set[Fence] = set()

        for pos in self.region:
            for dir, fd in zip(DIRS, FENCE_DIRS):
                border_pos = Fence(pos.row * 2 + dir.row, pos.col * 2 + dir.col, fd)
                if border_pos in borders:
                    borders.remove(border_pos)
                else:
                    borders.add(border_pos)

        horizontal_borders: dict[tuple[int, str], list[int]] = defaultdict(list)
        vertical_borders: dict[tuple[int, str], list[int]] = defaultdict(list)

        # Odd rows are horizontal

        for pos in borders:
            if pos.row % 2 == 1:
                horizontal_borders[(pos.row, pos.dir)].append(pos.col)
            else:
                vertical_borders[(pos.col, pos.dir)].append(pos.row)

        num_borders = 0

        for vals in vertical_borders.values():
            vals.sort()
            num_borders += 1
            for i in range(1, len(vals)):
                if vals[i] - vals[i - 1] > 2:
                    num_borders += 1
            # print(vals, num_borders)

        for vals in horizontal_borders.values():
            vals.sort()
            num_borders += 1
            for i in range(1, len(vals)):
                if vals[i] - vals[i - 1] > 2:
                    num_borders += 1

            # print(vals, num_borders)

        # print(self.val)
        # print(vertical_borders)
        # print(horizontal_borders)

        return num_borders


def load_data(filename: str) -> Farm:
    map: list[list[str]] = []

    with open(filename, "r") as f:
        for line in f.readlines():
            map.append([*line.strip()])

    farm = Farm(map)
    return farm


def find_region(farm: Farm, start: PlantPos, visited: set[PlantPos]) -> Region:
    q: deque[PlantPos] = deque()
    q.append(start)
    pos_val = farm.get_val(start)
    region: list[PlantPos] = []

    while q:
        cur = q.popleft()
        visited.add(cur)
        region.append(cur)

        for dir in DIRS:
            next_point = PlantPos(cur.row + dir.row, cur.col + dir.col)
            if farm.within_range(next_point) is False:
                continue

            if next_point in visited:
                continue

            next_val = farm.get_val(next_point)

            if next_point not in q and next_val == pos_val:
                q.append(next_point)
    res = Region(region, pos_val)
    return res


def solve_part_one(farm: Farm) -> int:
    farm = deepcopy(farm)
    visited: set[PlantPos] = set()
    cur = PlantPos(0, 0)

    while farm.within_range(cur):
        if cur in visited:
            cur = farm.get_next_val(cur)
            continue
        region = find_region(farm, cur, visited)
        farm.regions.append(region)
        cur = farm.get_next_val(cur)

    # for region in farm.regions:
    #     print(region)

    return farm.get_cost()


def solve_part_two(farm: Farm) -> int:
    farm = deepcopy(farm)
    visited: set[PlantPos] = set()
    cur = PlantPos(0, 0)

    while farm.within_range(cur):
        if cur in visited:
            cur = farm.get_next_val(cur)
            continue
        region = find_region(farm, cur, visited)
        farm.regions.append(region)
        cur = farm.get_next_val(cur)

    # for region in farm.regions:
    #     print(region)

    return farm.get_cost_part_two()


def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    farm = load_data(filename)
    print(solve_part_one(farm))
    print(solve_part_two(farm))
