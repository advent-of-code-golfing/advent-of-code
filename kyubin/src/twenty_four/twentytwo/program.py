from copy import deepcopy
from dataclasses import dataclass
from collections import defaultdict

from src.utils import get_input_filename


@dataclass
class Sequence:
    first: int
    second: int
    third: int
    fourth: int

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Sequence):
            return False
        return (
            self.first == value.first
            and self.second == value.second
            and self.third == value.third
            and self.fourth == value.fourth
        )

    def __hash__(self) -> int:
        return hash((self.first, self.second, self.third, self.fourth))


def load_data(filename: str) -> list[int]:
    res: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            res.append(int(line))
    return res


def generate_secret_number(num: int) -> int:
    # Mulitply by 64, mix this value into secret number
    num = num ^ (num * 64)
    # prune
    num = num % 16777216
    # Divide by 32, round down, mix into secret number
    num = num ^ (num // 32)
    # Prune
    num = num % 16777216
    # Multiply number by 2024, mix
    num = num ^ (num * 2048)
    # Prune
    num = num % 16777216
    return num


def solve_part_one(data: list[int]) -> int:
    tot = 0
    for num in data:
        for _ in range(2000):
            num = generate_secret_number(num)
        # print(num)
        tot += num
    return tot


def solve_part_two(data: list[int]) -> float:
    prices: list[list[int]] = []
    for num in data:
        cur_sequence: list[int] = []
        cur_sequence.append(num % 10)
        for _ in range(2000):
            num = generate_secret_number(num)
            cur_sequence.append(num % 10)
        # print(cur_sequence)
        prices.append(cur_sequence)

    diffs: list[list[int]] = []
    for price in prices:
        diffs.append([price[i] - price[i - 1] for i in range(1, len(price))])
    # print(len(diffs[0]))

    # print(diffs)

    # print(diffs)
    # Store dictionary of dict[sequence: price_to_sell] for each of the diffs
    unique_sequences: set[Sequence] = set()
    max_prices: list[dict[Sequence, int]] = []
    total_max_price_per_seq: dict[Sequence, int] = defaultdict(int)
    for num_idx, diff in enumerate(diffs):
        max_price_per_seq: dict[Sequence, int] = {}
        for i in range(3, len(diff)):
            sequence = Sequence(diff[i - 3], diff[i - 2], diff[i - 1], diff[i])
            # num_idx + i because no diff price for first
            val_to_sell = prices[num_idx][i + 1]
            unique_sequences.add(sequence)
            if sequence in max_price_per_seq:
                continue
            max_price_per_seq[sequence] = val_to_sell
            total_max_price_per_seq[sequence] += val_to_sell
        max_prices.append(max_price_per_seq)

    return max(total_max_price_per_seq.values())


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
