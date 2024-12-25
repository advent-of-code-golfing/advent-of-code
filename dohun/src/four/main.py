from src.utils import get_input_filename
from collections import Counter

import numpy as np
import copy


def load_data(filename: str) -> tuple[list[int], list[int]]:
    str_list: list[str] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            str_list.append(list(line.split()[0]))

        return np.array(str_list)


def q1(str_list: list[str]) -> int:
    search_array: list[str] = []
    num_rows = len(str_list)
    num_cols = len(str_list[0])

    for i in range(num_rows):
        for j in range(num_cols):
            if i <= num_rows - 4:
                search_array.append("".join(str_list[i : i + 4, j]))

            if j <= num_cols - 4:
                search_array.append("".join(str_list[i, j : j + 4]))

            if i <= num_rows - 4 and j <= num_cols - 4:
                search_array.append(
                    "".join(
                        [
                            str_list[i, j]
                            for i, j in zip(range(i, i + 4), range(j, j + 4))
                        ]
                    )
                )

            if i <= num_rows - 4 and j >= 3:
                search_array.append(
                    str_list[i, j]
                    + str_list[i + 1, j - 1]
                    + str_list[i + 2, j - 2]
                    + str_list[i + 3, j - 3]
                )

    reverse_search_array = [x[::-1] for x in search_array if len(x) == 4]

    full_search_array = search_array + reverse_search_array
    str_counter = Counter(full_search_array)

    return str_counter["XMAS"]


def q2(str_list: list[str]) -> int:
    count = 0
    num_rows = len(str_list)
    num_cols = len(str_list[0])

    for i in range(num_rows - 2):
        for j in range(num_cols - 2):
            str_1 = str_list[i, j] + str_list[i + 1, j + 1] + str_list[i + 2, j + 2]

            if str_1 == "MAS" or str_1[::-1] == "MAS":
                str_2 = str_list[i + 2, j] + str_list[i + 1, j + 1] + str_list[i, j + 2]

                if str_2 == "MAS" or str_2[::-1] == "MAS":
                    count += 1

    return count


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    str_list = load_data(filename)
    print(q1(str_list))
    print(q2(str_list))
