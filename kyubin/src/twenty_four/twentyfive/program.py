from copy import deepcopy

from src.utils import get_input_filename


class KeyLock:
    def __init__(self, pattern: list[str]) -> None:
        self.pattern = pattern

    def pprint(self) -> None:
        for line in self.pattern:
            print(line)

    def is_lock(self) -> bool:
        return self.pattern[0][0] == "#"

    def is_key(self) -> bool:
        return not self.is_lock()

    def heights(self) -> list[int]:
        heights = [-1] * 5

        for line in self.pattern:
            for i, val in enumerate(line):
                if val == "#":
                    heights[i] += 1
        return heights


def load_data(filename: str) -> list[KeyLock]:
    res: list[KeyLock] = []
    with open(filename, "r") as f:
        cur: list[str] = []
        for line in f.readlines():
            line = line.strip()
            if not line:
                kl = KeyLock(cur)
                res.append(kl)
                cur = []
            else:
                cur.append(line)

    res.append(KeyLock(cur))
    return res


def part_one(input: list[KeyLock]) -> int:
    keys: list[KeyLock] = []
    locks: list[KeyLock] = []
    for kl in input:
        if kl.is_key():
            keys.append(kl)
        else:
            locks.append(kl)

    fits = 0

    for key in keys:
        for lock in locks:
            fit = True
            for k, t in zip(key.heights(), lock.heights()):
                if k + t >= 6:
                    fit = False
                    break
            if fit:
                fits += 1
    return fits


def run(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    input = load_data(filename)
    print(part_one(deepcopy(input)))


if __name__ == "__main__":
    run(False)
