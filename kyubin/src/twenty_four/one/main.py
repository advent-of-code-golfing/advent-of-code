from collections import Counter

from kyubin.src.utils import get_input_filename


def load_data(filename: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
    return left, right


def part_one(left: list[int], right: list[int]) -> int:
    left.sort()
    right.sort()
    res = 0

    for l, r in zip(left, right):
        res += abs(l - r)
    return res


def part_two(left: list[int], right: list[int]) -> int:
    right_counter = Counter(right)
    score = 0
    for num in left:
        if num not in right_counter:
            continue
        freq = right_counter[num]
        score += freq * num
    return score


if __name__ == "__main__":
    filename = get_input_filename(__file__)
    left, right = load_data(filename)
    print(part_one(left, right))
    left, right = load_data(filename)
    print(part_two(left, right))
