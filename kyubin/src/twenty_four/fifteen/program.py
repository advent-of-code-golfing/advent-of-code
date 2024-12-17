from dataclasses import dataclass
import re
import time
from copy import deepcopy

from src.common import Vector
from src.utils import get_input_filename


@dataclass
class Map:
    map: list[list[str]]
    movements: str
    pos: Vector

    def print_map(self) -> None:
        for m in self.map:
            print("".join(m))

    def move_right(self) -> None:
        row, col = self.pos.row, self.pos.col

        vals = ["@"]

        while True:
            col += 1
            cur_val = self.map[row][col]
            match cur_val:
                case "#":
                    # Rock
                    return
                case "O":
                    vals.append("O")
                    continue
                case ".":
                    # Free space, can put a space in the original location
                    vals.insert(0, ".")
                    break
        i = 0
        for c in range(self.pos.col, col + 1):
            self.map[row][c] = vals[i]
            i += 1
        self.pos = Vector(self.pos.row, self.pos.col + 1)

    def move_left(self) -> None:
        row, col = self.pos.row, self.pos.col

        vals = ["@"]

        while True:
            col -= 1
            cur_val = self.map[row][col]
            match cur_val:
                case "#":
                    # Rock
                    return
                case "O":
                    vals.append("O")
                    continue
                case ".":
                    # Free space, can put a space in the original location
                    vals.insert(0, ".")
                    break
        i = 0
        for c in range(self.pos.col, col - 1, -1):
            self.map[row][c] = vals[i]
            i += 1
        self.pos = Vector(self.pos.row, self.pos.col - 1)

    def move_up(self) -> None:
        row, col = self.pos.row, self.pos.col

        vals = ["@"]

        while True:
            row -= 1
            cur_val = self.map[row][col]
            match cur_val:
                case "#":
                    # Rock
                    return
                case "O":
                    vals.append("O")
                    continue
                case ".":
                    # Free space, can put a space in the original location
                    vals.insert(0, ".")
                    break
        i = 0
        for r in range(self.pos.row, row - 1, -1):
            self.map[r][col] = vals[i]
            i += 1
        self.pos = Vector(self.pos.row - 1, self.pos.col)

    def move_down(self) -> None:
        row, col = self.pos.row, self.pos.col

        vals = ["@"]

        while True:
            row += 1
            cur_val = self.map[row][col]
            match cur_val:
                case "#":
                    # Rock
                    return
                case "O":
                    vals.append("O")
                    continue
                case ".":
                    # Free space, can put a space in the original location
                    vals.insert(0, ".")
                    break
        i = 0
        for r in range(self.pos.row, row + 1):
            self.map[r][col] = vals[i]
            i += 1
        self.pos = Vector(self.pos.row + 1, self.pos.col)

    def calculate_gps(self) -> int:
        total = 0
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] != "O":
                    continue
                total += row * 100 + col
        return total
    

def load_data(filename: str) -> Map:
    reading_map = True
    map = []
    movements = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if not line:
                reading_map = False
                continue
            if reading_map:
                map.append([*line])
            else:
                movements += line
    # Find starting point
    for r in range(len(map)):
        for c in range(len(map[0])):
            if map[r][c] == "@":
                start = Vector(r, c)
                break
    instructions = Map(map, movements, start)
    return instructions


def solve_part_one(map: Map) -> int:
    map.print_map()
    for ins in map.movements:
        match ins:
            case ">":
                # print("RIGHT")
                map.move_right()
                # print(map.pos)
                # map.print_map()
            case "<":
                # print("LEFT")
                map.move_left()
                # print(map.pos)
                # map.print_map()
            case "^":
                # print("UP")
                map.move_up()
                # print(map.pos)
                # map.print_map()
            case "v":
                # print("DOWN")
                map.move_down()
                # print(map.pos)
                # map.print_map()
    return map.calculate_gps()


def solve_part_two(data: Map) -> int: ...


def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)

    if test:
        print(solve_part_one(deepcopy(data)))
        print(solve_part_two(deepcopy(data)))
    else:
        print(solve_part_one(deepcopy(data)))
        print(solve_part_two(deepcopy(data)))


if __name__ == "__main__":
    run_program(False)
