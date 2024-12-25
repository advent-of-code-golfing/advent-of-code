from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


def load_data(filename: str, is_test=False) -> list:
    initial_num_list = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            nums = int(line.strip())
            initial_num_list.append(nums)
    if is_test:
        return np.array([1, 2, 3, 2024])
    return np.array(initial_num_list)


class Buyer:
    def __init__(self, initial_num: int):
        self.secret_num = initial_num

    def calculate_secret_num(self, num_iterations: int, storage_dict: dict = dict()):
        previous_num = None
        diffs_list = list()
        my_storage_dict = dict()
        for i in range(num_iterations):
            self.process()
            if i > 0:
                diff = (self.secret_num % 10) - (previous_num % 10)
                diffs_list.append(diff)
            previous_num = copy.copy(self.secret_num)
            if i > 3:
                diffs_tuple = (
                    diffs_list[i - 4],
                    diffs_list[i - 3],
                    diffs_list[i - 2],
                    diffs_list[i - 1],
                )

                if diffs_tuple not in my_storage_dict:
                    if diffs_tuple in storage_dict:
                        storage_dict[diffs_tuple] += self.secret_num % 10
                    else:
                        storage_dict[diffs_tuple] = self.secret_num % 10

                    my_storage_dict[diffs_tuple] = self.secret_num % 10

        return storage_dict

    def mix(self, value: int):
        return value ^ self.secret_num

    def prune(self):
        self.secret_num = self.secret_num % 16777216

    def process(self):
        self.secret_num = self.mix(self.secret_num * 64)
        self.prune()
        self.secret_num = self.mix(self.secret_num // 32)
        self.prune()
        self.secret_num = self.mix(self.secret_num * 2048)
        self.prune()


def q1(
    initial_num_list: list,
) -> int:
    secret_sum = 0
    for initial_num in initial_num_list:
        buyer = Buyer(initial_num)
        buyer.calculate_secret_num(2000)
        secret_sum += buyer.secret_num
    return secret_sum


def q2(initial_num_list: list) -> int:
    storage_dict = dict()
    for i, initial_num in enumerate(initial_num_list):
        buyer = Buyer(initial_num)
        storage_dict = buyer.calculate_secret_num(2000, storage_dict)

    num_bananas = [int(x) for x in storage_dict.values()]
    return max(num_bananas)


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    initial_num_list = load_data(filename, is_test=False)
    print(q1(initial_num_list))
    print(q2(initial_num_list))
