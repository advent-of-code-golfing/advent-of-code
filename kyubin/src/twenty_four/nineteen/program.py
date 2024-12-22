from copy import deepcopy
from functools import cache

from src.utils import get_input_filename


class Onsen:
    def __init__(self, towels: list[str], patterns: list[str]) -> None:
        self.towels = towels
        self.patterns = patterns

    @cache
    def pattern_possible(self, pattern: str) -> bool:
        for towel in self.towels:
            if pattern == towel:
                return True
            if pattern.startswith(towel):
                possible = self.pattern_possible(pattern[len(towel) :])
                if possible is True:
                    return True
        return False

    @cache
    def get_num_combinations(self, pattern: str) -> int:
        """
        Get number of different combinations a pattern can be created.

        Returns -1 if a pattern cannot be created.
        """
        total_num = 0
        for towel in self.towels:
            if pattern == towel:
                total_num += 1
                continue
            if pattern.startswith(towel):
                patterns = self.get_num_combinations(pattern[len(towel) :])
                if patterns == -1:
                    continue
                else:
                    total_num += patterns

        if total_num == 0:
            return -1
        return total_num


def load_data(filename: str):
    patterns: list[str] = []
    with open(filename, "r") as f:
        towels_raw = f.readline()
        towels: list[str] = [t.strip() for t in towels_raw.split(",")]

        f.readline()
        for line in f.readlines():
            patterns.append(line.strip())

    onsen = Onsen(towels, patterns)
    return onsen


def solve_part_one(onsen: Onsen) -> int:
    possible = 0
    for pattern in onsen.patterns:
        if onsen.pattern_possible(pattern):
            possible += 1
    return possible


def solve_part_two(onsen: Onsen) -> int:
    num_combinations = 0
    for pattern in onsen.patterns:
        nums = onsen.get_num_combinations(pattern)
        # print(nums, pattern)
        if nums > 0:
            num_combinations += nums
    return num_combinations


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
