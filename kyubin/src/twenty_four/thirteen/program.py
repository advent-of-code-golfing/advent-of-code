from dataclasses import dataclass
import sys
import re


sys.path.append(".")

from src.utils import get_input_filename


@dataclass
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def __str__(self) -> str:
        return f"A: {self.button_a}, B: {self.button_b}, Prize: {self.prize}"

    def solve_system(self) -> int:
        # Ax = b
        # x = A-1 p
        # Where p is the prize
        # Analytical solution using matrix inverse
        # A = [ a, b]
        #     [ c, d]
        #
        # A = 1 / (a * d - b * c) * (d * p1 - b * p2)
        # B = 1 / (a * d - b * c) * (-c * p1 + a * p2)

        a = self.button_a[0]
        b = self.button_b[0]
        c = self.button_a[1]
        d = self.button_b[1]
        p1 = self.prize[0]
        p2 = self.prize[1]

        det = a * d - b * c

        # No solution
        if det == 0:
            print("No sol!")
            return 0

        a_clicks = 1 / det * (d * p1 - b * p2)
        b_clicks = 1 / det * (-c * p1 + a * p2)

        # print(a_clicks, b_clicks)

        if a_clicks < 0 or b_clicks < 0:
            return 0

        # Verificaion
        a_clicks = round(a_clicks)
        b_clicks = round(b_clicks)

        if (a * a_clicks + b * b_clicks == p1) and (c * a_clicks + d * b_clicks == p2):
            return a_clicks * 3 + b_clicks

        return 0


def load_data(filename: str) -> list[Machine]:
    machines: list[Machine] = []
    current: list[tuple[int, int]] = []
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
    machines.append(Machine(*current))
    return machines


def solve_part_one(machines: list[Machine]) -> int:
    res = 0
    for m in machines:
        # print("-------")
        val = m.solve_system()
        res += val
        # print(m, val)
    return res


def solve_part_two(machines: list[Machine]) -> int:
    res = 0
    for m in machines:
        m.prize = (m.prize[0] + 10000000000000, m.prize[1] + 10000000000000)
        # print("-------")
        val = m.solve_system()
        res += val
        # print(m, val)
    return res


def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)
    print(solve_part_one(data))
    print(solve_part_two(data))


if __name__ == "__main__":
    run_program(False)
