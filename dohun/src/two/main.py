from src.utils import get_input_filename
import numpy as np
import copy


def load_data(filename: str) -> tuple[list[int], list[int]]:
    input_list: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            nums = line.strip().split()
            input_list.append([int(l) for l in nums])

    return input_list


def _check_if_report_ok(input: list, lives=1):
    len_input = len(input)
    prev_diff = None

    current_life = lives
    i = 0
    while current_life >= 1 and i < len_input:
        if i == len_input - 1:
            return 1

        next = i + 1
        diff = input[next] - input[i]
        if abs(diff) >= 1 and abs(diff) <= 3:
            if prev_diff is None:
                prev_diff = diff
                i = i + 1
                continue
            if prev_diff * diff > 0:
                prev_diff = diff
                i = i + 1
            else:
                current_life -= 1
        else:
            current_life -= 1

    return 0


def q1(input_list: list) -> int:
    count = 0
    for input in input_list:
        count += _check_if_report_ok(input)

    return count


def q2(input_list: list) -> int:
    count = 0
    for input in input_list:
        ok = _check_if_report_ok(input)
        if ok:
            count += 1
        else:
            len_input = len(input)
            for i in range(len_input):
                remove_ok = _check_if_report_ok(input[:i] + input[i + 1 :])
                if remove_ok:
                    count += 1
                    break

    return count


def q2_nice(input_list: list) -> int:
    count = 0
    for input in input_list:
        count += _check_if_report_ok(input, lives=2)

    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    input_list = load_data(filename)
    print(q1(input_list))
    print(q2(input_list))
    print(q2_nice(input_list))
