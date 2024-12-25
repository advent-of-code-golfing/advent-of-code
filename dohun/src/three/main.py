from src.utils import get_input_filename
import numpy as np
import copy


def load_data(filename: str) -> tuple[list[int], list[int]]:
    str_to_parse: str = ""
    with open(filename, "r") as f:
        for line in f.readlines():
            str_to_parse = str_to_parse + line

        return str_to_parse


def q1(input_str: str) -> int:
    count = 0
    for i in range(len(input_str)):
        if input_str[i : i + 4] == "mul(":
            k = i + 4
            while input_str[k].isdigit():
                k = k + 1
            if input_str[k] != ",":
                i = k
                continue
            int_1 = int(input_str[i + 4 : k])
            j = k + 1
            while input_str[j].isdigit():
                j = j + 1
            if input_str[j] != ")":
                i = j
                int_1 = None
                continue
            int_2 = int(input_str[k + 1 : j])
            count += int_1 * int_2
            i = j + 1

    return count


def q2(input_str: str) -> int:
    count = 0
    do = True
    for i in range(len(input_str)):
        if input_str[i : i + 4] == "do()":
            do = True
        if input_str[i : i + 7] == "don't()":
            do = False

        if input_str[i : i + 4] == "mul(":
            k = i + 4
            while input_str[k].isdigit():
                k = k + 1
            if input_str[k] != ",":
                i = k
                continue
            int_1 = int(input_str[i + 4 : k])
            j = k + 1
            while input_str[j].isdigit():
                j = j + 1
            if input_str[j] != ")":
                i = j
                int_1 = None
                continue
            int_2 = int(input_str[k + 1 : j])
            if do:
                count += int_1 * int_2
            i = j + 1

    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    str_to_parse = load_data(filename)
    print(q1(str_to_parse))
    print(q2(str_to_parse))
