from copy import deepcopy
from collections import defaultdict, deque
from dataclasses import dataclass
from src.utils import get_input_filename


@dataclass
class Cluster:
    first: str
    second: str
    third: str

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Cluster):
            raise ValueError
        return sorted([self.first, self.second, self.third]) == sorted(
            [value.first, value.second, value.third]
        )


class Computer:
    def __init__(self, val: str) -> None:
        self.val = val
        self.previous: set[str] = set()

    def __str__(self) -> str:
        return self.val

    def __repr__(self) -> str:
        return self.val

    def __hash__(self) -> int:
        return hash(self.val)

    def __eq__(self, value: object) -> bool:
        if not (isinstance(value, Computer)):
            raise ValueError
        return self.val == value.val

    def connected_to_all_previous(self, connections: set[str]) -> bool:
        for prev in self.previous:
            if prev not in connections:
                return False
        return True

    def network(self) -> set[str]:
        network = deepcopy(self.previous)
        network.add(self.val)
        return network


class ComputerMap:
    def __init__(self, connections: list[str]) -> None:
        self.computers: set[str] = set()
        self.computer_map: dict[str, set[str]] = defaultdict(set)
        self.generate_map(connections)

    def generate_map(self, connections: list[str]) -> None:
        for connection in connections:
            c1, c2 = connection.split("-")
            self.computers.add(c1)
            self.computers.add(c2)
            self.computer_map[c1].add(c2)
            self.computer_map[c2].add(c1)

    def generate_groups_of_three(self) -> list[Cluster]:
        # We can only check ones that start in t
        threes: list[Cluster] = []

        for computer in self.computers:
            if computer.startswith("t") is False:
                continue
            for level_one in self.computer_map[computer]:
                if level_one == computer:
                    continue
                for level_two in self.computer_map[level_one]:
                    if level_two == computer or level_two == level_one:
                        continue
                    if computer not in self.computer_map[level_two]:
                        continue
                    cluster = Cluster(computer, level_one, level_two)
                    if cluster not in threes:
                        threes.append(cluster)
        return threes

    def find_largest_set_with_computer(self, computer: str) -> set[str]:
        # Using BFS
        cur = Computer(computer)
        queue: deque[Computer] = deque()
        queue.append(cur)

        current_max: set[str] = set()
        been: set[str] = set()

        while queue:
            cur = queue.pop()
            been.add(cur.val)

            if len(cur.previous) + 1 > len(current_max):
                current_max = cur.network()
            # Check all the neighbours
            for neighbour in self.computer_map[cur.val]:
                if neighbour in been:
                    continue
                neighbour_computer = deepcopy(cur)
                neighbour_computer.val = neighbour
                if cur.connected_to_all_previous(self.computer_map[neighbour]):
                    neighbour_computer.previous.add(cur.val)
                    queue.append(neighbour_computer)
        return current_max

    def find_largest_set(self) -> list[str]:
        current_max: set[str] = set()

        for i, computer in enumerate(self.computers):
            # print(i)
            network = self.find_largest_set_with_computer(computer)
            if len(network) > len(current_max):
                current_max = network

        return sorted(current_max)


def load_data(filename: str) -> list[str]:
    connections: list[str] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            connections.append(line.strip())
    return connections


def solve_part_one(data: list[str]) -> int:
    computer_map = ComputerMap(data)
    threes = computer_map.generate_groups_of_three()
    # print(threes)
    return len(threes)


def solve_part_two(data: list[str]) -> str:
    computer_map = ComputerMap(data)
    return ",".join(computer_map.find_largest_set())


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
