from copy import deepcopy

from src.utils import get_input_filename


def load_data(filename: str) -> list[str]:
    lines: list[str] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            lines.append(line.strip())

    return lines


def solve_part_one(data: list[str]) -> int: ...


def solve_part_two(data: list[str]) -> int: ...


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
