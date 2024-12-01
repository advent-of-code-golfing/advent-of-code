from collections import Counter

from src.utils import get_input_filename


def load_data(filename: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
    return left, right


def part_one(filename: str) -> int:
    left, right = load_data(filename)

    left.sort()
    right.sort()
    res = 0

    for l, r in zip(left, right):
        res += abs(l - r)
    return res


def part_two(filename: str) -> int:
    left, right = load_data(filename)
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

    print(part_one(filename))
    print(part_two(filename))
