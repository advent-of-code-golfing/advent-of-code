from dataclasses import dataclass
import re

from src.common import Vector
from src.utils import get_input_filename
import time


@dataclass
class Robot:
    pos: Vector
    vel: Vector


def load_data(filename: str) -> list[Robot]:
    robots: list[Robot] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            coords = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", line)[0]
            coords = [int(n) for n in coords]
            start = Vector(coords[1], coords[0])
            vel = Vector(coords[3], coords[2])
            r = Robot(start, vel)
            robots.append(r)
    return robots


def assign_quadrant(robot: Robot, nrows: int, ncols: int) -> int:
    # Always odd, we do it based on the mid line

    v_mid = ncols // 2
    h_mid = nrows // 2

    if robot.pos.col < v_mid and robot.pos.row < h_mid:
        return 1

    if robot.pos.col > v_mid and robot.pos.row < h_mid:
        return 2

    if robot.pos.col < v_mid and robot.pos.row > h_mid:
        return 3

    if robot.pos.col > v_mid and robot.pos.row > h_mid:
        return 4

    return -1


def solve_part_one(robots: list[Robot], nrows: int, ncols: int) -> int:
    # 100 seconds
    # print(robots)
    counts = {-1: 0, 1: 0, 2: 0, 3: 0, 4: 0}
    for robot in robots:
        new_pos = robot.pos + Vector(robot.vel.row * 100, robot.vel.col * 100)
        new_pos.row = new_pos.row % nrows
        if new_pos.row < 0:
            new_pos.row += nrows
        new_pos.col = new_pos.col % ncols
        if new_pos.col < 0:
            new_pos.col += ncols
        robot.pos = new_pos
        quad = assign_quadrant(robot, nrows, ncols)
        # print(new_pos, quad)

        counts[quad] += 1

    # print(counts)

    total = 1
    for i in range(1, 5):
        total *= counts[i]

    return total


def plot(robots: list[Robot], nrows: int, ncols: int) -> None:
    vals = [["-" for _ in range(ncols)] for _ in range(nrows)]

    for robot in robots:
        vals[robot.pos.row][robot.pos.col] = "O"

    print("#" * (nrows + 10))
    for val in vals:
        print("".join(val))


def check_if_easter_egg(robots: list[Robot], nrows: int, ncols: int, n: int) -> bool:
    vals = [["-" for _ in range(ncols)] for _ in range(nrows)]

    for robot in robots:
        vals[robot.pos.row][robot.pos.col] = "O"

    # If middle n x n are all no robots, we can assume its an egg shaped form

    mid_row_start = nrows // 2 - n // 2
    mid_col_start = ncols // 2 - n // 2

    for r in range(mid_row_start, mid_row_start + n):
        for c in range(mid_col_start, mid_col_start + n):
            if vals[r][c] == "O":
                return False
    return True


def solve_part_two(robots: list[Robot], nrows: int, ncols: int) -> int:
    seconds = 1
    plot(robots, nrows, ncols)
    while True:
        for robot in robots:
            new_pos = robot.pos + Vector(robot.vel.row, robot.vel.col)
            new_pos.row = new_pos.row % nrows
            if new_pos.row < 0:
                new_pos.row += nrows
            new_pos.col = new_pos.col % ncols
            if new_pos.col < 0:
                new_pos.col += ncols
            robot.pos = new_pos

        if check_if_easter_egg(robots, nrows, ncols, 15):
            print(seconds)
            plot(robots, nrows, ncols)
        seconds += 1


def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)
    if test:
        print(solve_part_one(data, 7, 11))
        print(solve_part_two(data, 7, 11))
    else:
        print(solve_part_one(data, 103, 101))
        print(solve_part_two(data, 103, 101))


if __name__ == "__main__":
    run_program(False)
