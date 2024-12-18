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
                    return
                case "O":
                    vals.append("O")
                    continue
                case "[":
                    vals.append("[")
                    continue
                case "]":
                    vals.append("]")
                    continue
                case ".":
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
                case "[":
                    vals.append("[")
                    continue
                case "]":
                    vals.append("]")
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

    def get_val(self, pos: Vector) -> str:
        return self.map[pos.row][pos.col]

    def can_move_in_dir(self, dir: Vector, pos: Vector, all_pos: set[Vector]) -> bool:
        # -1 for up, +1 for down
        # Base cases

        cur_val = self.get_val(pos)
        if cur_val == ".":
            return True
        elif cur_val == "#":
            return False
        elif cur_val == "@":
            can_move = self.can_move_in_dir(dir, pos + dir, all_pos)
            all_pos.add(pos)
            return can_move
        elif cur_val == "[":
            right = Vector(0, 1)
            can_move = self.can_move_in_dir(
                dir, pos + right + dir, all_pos
            ) and self.can_move_in_dir(dir, pos + dir, all_pos)
            all_pos.add(pos)
            all_pos.add(pos + right)
            return can_move

        elif cur_val == "]":
            left = Vector(0, -1)
            can_move = self.can_move_in_dir(
                dir, pos + dir + left, all_pos
            ) and self.can_move_in_dir(dir, pos + dir, all_pos)
            all_pos.add(pos)
            all_pos.add(pos + left)
            return can_move

    def move_in_dir(self, dir: Vector, all_pos: set[Vector]) -> bool:
        # Sort first
        # If dir is up (-1), in increasing row
        # otherwise, in decreasing row
        all_pos = list(all_pos)
        all_pos.sort(key=lambda pos: pos.row, reverse=dir.row > 0)
        print(all_pos)
        for pos in all_pos:
            to_swap = pos + dir
            self.map[pos.row][pos.col], self.map[to_swap.row][to_swap.col] = (
                self.map[to_swap.row][to_swap.col],
                self.map[pos.row][pos.col],
            )

    def move_up_part_two(self) -> None:
        all_pos = set()
        up = Vector(-1, 0)
        if self.can_move_in_dir(up, self.pos, all_pos):
            self.move_in_dir(up, all_pos)
            self.pos = self.pos + up

    def move_down_part_two(self) -> None:
        all_pos = set()
        down = Vector(1, 0)
        if self.can_move_in_dir(down, self.pos, all_pos):
            print(all_pos)
            self.move_in_dir(down, all_pos)
            self.pos = self.pos + down

    def calculate_gps_part_two(self) -> int:
        total = 0
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] != "[":
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


def modify_data(data: Map) -> Map:
    new_map = []

    for row in data.map:
        new_row = []
        for val in row:
            match val:
                case "#":
                    new_row.extend(["#", "#"])
                case "O":
                    new_row.extend(["[", "]"])
                case ".":
                    new_row.extend([".", "."])
                case "@":
                    new_row.extend(["@", "."])
        new_map.append(new_row)

    for r in range(len(new_map)):
        for c in range(len(new_map[0])):
            if new_map[r][c] == "@":
                start = Vector(r, c)
                break

    new_data = Map(new_map, data.movements, start)
    return new_data


def solve_part_two(data: Map) -> int:
    map = modify_data(data)
    # Left and right not impacted, only up or down
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
                map.move_up_part_two()
                # print(map.pos)
                # map.print_map()
            case "v":
                # print("DOWN")
                map.move_down_part_two()
                # print(map.pos)/
                # map.print_map()
    return map.calculate_gps_part_two()


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
