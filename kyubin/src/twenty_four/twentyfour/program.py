from copy import deepcopy
from collections import OrderedDict
from dataclasses import dataclass
import re

from src.utils import get_input_filename


@dataclass
class Equation:
    operand_one: str
    operation: str
    operand_two: str
    result: str

    def __str__(self) -> str:
        return (
            f"{self.operand_one} {self.operation} {self.operand_two} -> {self.result}"
        )

    def lhs(self) -> str:
        return f"({self.operand_one} {self.operation} {self.operand_two})"


InputData = tuple[dict[str, int], list[Equation]]


def load_data(filename: str) -> InputData:
    values: dict[str, int] = {}
    equations: list[Equation] = []
    reading_values = True
    with open(filename, "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                reading_values = False
                continue

            if reading_values:
                var, val = line.strip().split(":")
                values[var] = int(val)
            else:
                equation = re.findall(r"(\w+)\s(\w+)\s(\w+)\s->\s(\w+)", line.strip())[
                    0
                ]
                equations.append(Equation(*equation))
    return values, equations


def get_unique_strings(data: InputData) -> set[str]:
    res: set[str] = set()
    values, equations = data
    for wire in values.keys():
        res.add(wire)

    for equation in equations:
        res.add(equation.operand_one)
        res.add(equation.operand_two)
        res.add(equation.result)

    return res


def solve_part_one(data: InputData) -> int:
    values, equations = data
    uniques = get_unique_strings(data)
    unique_count = len(uniques)

    equations.sort(key=lambda x: (x.operand_one, x.operand_two), reverse=True)

    while len(values) != unique_count:
        for equation in equations:
            if equation.operand_one not in values or equation.operand_two not in values:
                continue

            if equation.result in values:
                continue

            v1, v2 = values[equation.operand_one], values[equation.operand_two]

            match equation.operation:
                case "AND":
                    values[equation.result] = v1 & v2
                case "OR":
                    values[equation.result] = v1 | v2
                case "XOR":
                    values[equation.result] = v1 ^ v2
                case _:
                    raise ValueError

    od = OrderedDict(sorted(values.items(), reverse=True))
    bin_string = "".join([str(v) for k, v in od.items() if k.startswith("z")])

    return int(bin_string, 2)


def backtrack(input: str, str_to_eq: dict[str, Equation]) -> str:

    if input[0] in ["x", "y", "z", "A", "X", "C", "T"]:
        return input

    equation = str_to_eq.get(input)
    if equation is None:
        return input

    operand_one_backtrack = backtrack(equation.operand_one, str_to_eq)
    operand_two_backtrack = backtrack(equation.operand_two, str_to_eq)

    return f"({operand_one_backtrack} {equation.operation} {operand_two_backtrack})"


def run_full_backtrack(equations: list[Equation]) -> None:
    str_to_eq = {equation.result: equation for equation in equations}
    
    print("-------BACKTRACKING-------")
    for i in range(46):
        z_str = f"z{i}" if i >= 10 else f"z0{i}"
        equation = str_to_eq[z_str]
        operand_one_backtrack = backtrack(equation.operand_one, str_to_eq)
        operand_two_backtrack = backtrack(equation.operand_two, str_to_eq)
        print(z_str)
        print(f"{operand_one_backtrack} {equation.operation} {operand_two_backtrack}")


def solve_part_two(data: InputData) -> int:
    # x value
    values, equations = data
    od = OrderedDict(sorted(values.items(), reverse=True))
    x_val = "".join([str(v) for k, v in od.items() if k.startswith("x")])
    y_val = "".join([str(v) for k, v in od.items() if k.startswith("y")])

    z_expected = int(x_val, 2) + int(y_val, 2)

    z_actual = solve_part_one(data)
    print("x___", x_val)
    print("y___", y_val)
    print("exp", f"{z_expected:b}")
    print("act", f"{z_actual:b}")

    # Comparing expected and what it must be,

    diff = z_expected ^ z_actual
    diff_str = f"{diff:b}"
    print("dif", diff_str)

    # z goes up to 25 bits
    # For this to work with ANY input values, z_i can and should only
    # depend on x and y bits less than or equal to i


    # For any given z_i, it should be in format
    # z_i = (x_i XOR y_i) XOR (carry from i - 1, we can call this c_{i - 1})
    # z_i = (x_i XOR y_i) XOR C_{i - 1}

    # The carry, C_i, is:
    # c_i = (x_i AND y_i) OR ((x_i XOR y_i) AND C_{i - 1})
    # i.e.
    # if both x_i and y_i are 1, then there is a carry
    # or if x_i or y_i are 1, and there is carry from i - 1

    # We can call x_i AND y_i A_i
    # And x_i XOR y_i X_oi
    # X_i AND C_{i - 1} = T_i
    # Then we know A_i OR T_i = C_i

    # This was added one by one specifically for my case, after running multiple times
    # and checking where it breaks
    changes = {
        ("nnf", "z09"),
        ("nhs", "z20"),
        ("ddn", "kqh"),
        ("wrc", "z34")
    }

    for change in changes:
        first, second = change[0], change[1]
        for equation in equations:
            if equation.result == first:
                equation.result = second
            elif equation.result == second:
                equation.result = first

    original_equations_with_switches = deepcopy(equations)

    changed_results: list[Equation] = []
    while True:
        # Keep track if there are changes to be made
        changed = False
        changes_to_make: dict[str, str] = {}

        for equation in equations:
            # Exception for i = 0, where x00 AND y00 = c00
            # if equation in changed_results:
            #     continue

            first_letter, first_num = equation.operand_one[0], equation.operand_one[1:]
            second_letter, second_num = equation.operand_two[0], equation.operand_two[1:]

            if not first_num.isdigit() and not second_num.isdigit():
                continue
            
            if equation.result.startswith("z"):
                continue

            letters = sorted([first_letter, second_letter])
            if letters == ["x", "y"] and first_num == second_num:
                if int(first_num) == 0 and equation.operation == "AND":
                    new_res = "C" + first_num
                else:
                    new_res = equation.operation[0] + first_num
                changes_to_make[equation.result] = new_res            
            elif letters == ["C", "X"] and equation.operation == "AND":
                # X_i AND C_{i - 1} = T_i, so
                diff = int(first_num) - int(second_num)
                if first_letter == "X" and diff == 1:
                    new_res = "T" + first_num
                elif first_letter == "C" and diff == -1:
                    new_res = "T" + second_num
                else:
                    pass
                changes_to_make[equation.result] = new_res

            elif letters == ["A", "T"] and equation.operation == "OR" and first_num == second_num:
                new_res = "C" + first_num
                changes_to_make[equation.result] = new_res
            # Exception case:
            else:
                continue
            changed_results.append(equation)
        
        for equation in equations:
            if equation.operand_one in changes_to_make and equation.operand_one != changes_to_make[equation.operand_one]:
                equation.operand_one = changes_to_make[equation.operand_one]
                changed = True
            if equation.operand_two in changes_to_make and equation.operand_two != changes_to_make[equation.operand_two]:
                equation.operand_two = changes_to_make[equation.operand_two]
                changed = True
            if equation.result in changes_to_make and equation.result != changes_to_make[equation.result]:
                equation.result = changes_to_make[equation.result]
                changed = True
        if not changed:
            break

    for equation in equations:
        print(equation)

    run_full_backtrack(equations)

    res = []
    for change in changes:
        res.extend([change[0], change[1]])
    res.sort()
    return ",".join(res)


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
