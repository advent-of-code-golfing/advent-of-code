import sys

sys.path.append(".")

from dataclasses import dataclass
import re

from src.utils import get_input_filename


@dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def __str__(self) -> str:
        return f"A: {self.button_a}, B: {self.button_b}, Prize: {self.prize}"


def load_data(filename: str) -> list[Machine]:
    machines: list[Machine] = []
    current = []
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.rstrip()
            if "Button A" in line:
                res = re.findall(r"Button A: X\+(\d+), Y\+(\d+)", line)[0]
                current.append((int(res[0]), int(res[1])))

            if "Button B" in line:
                res = re.findall(r"Button B: X\+(\d+), Y\+(\d+)", line)[0]
                current.append((int(res[0]), int(res[1])))

            if "Prize" in line:
                res = re.findall(r"Prize: X\=(\d+), Y\=(\d+)", line)[0]
                current.append((int(res[0]), int(res[1])))

            if not line:
                machines.append(Machine(*current))
                current = []
    return machines


def solve_part_one(machines: list[Machine]) -> int: ...


def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)
    print(data)
    # print(part_one(left, right))
    # left, right = load_data(filename)
    # print(part_two(left, right))


if __name__ == "__main__":

    run_program(True)
