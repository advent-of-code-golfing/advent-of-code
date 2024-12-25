from src.utils import get_input_filename
import numpy as np


def load_data(filename: str) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            l, r = line.strip().split()
            left.append(int(l))
            right.append(int(r))
    return left, right


def q1(left: list, right: list) -> int:
    left.sort()
    right.sort()

    dist = sum([abs(x - y) for x, y, in zip(left, right)])
    return dist


def q2(left: list, right: list) -> int:
    left = np.array(left)
    right = np.array(right)

    score = 0
    for i in left:
        matches = int(sum(i == right))
        score += matches * i

    return score


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    left, right = load_data(filename)
    print(q1(left, right))
    print(q2(left, right))
