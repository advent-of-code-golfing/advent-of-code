from copy import deepcopy
from dataclasses import dataclass
from typing import Callable
from src.utils import get_input_filename
from functools import cache, partial


@dataclass
class ProgramInput:
    register_a: int
    register_b: int
    register_c: int
    instruction: int
    commands: list[int]
    out: str = ""

    def __hash__(self) -> int:
        return hash(
            (self.register_a, self.register_b, self.register_c, self.instruction)
        )


def copy_input(input: ProgramInput) -> ProgramInput:
    res = deepcopy(input)
    res.out = ""
    return res


class Program:
    def __init__(self, a: int, b: int, c: int, commands: list[int]) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.commands = commands

    @staticmethod
    def combo(combo: int, input: ProgramInput) -> int:
        if combo <= 3:
            return combo
        elif combo == 4:
            return input.register_a
        elif combo == 5:
            return input.register_b
        elif combo == 6:
            return input.register_c
        raise

    @staticmethod
    def adv(combo: int, input: ProgramInput) -> ProgramInput:
        input.register_a = input.register_a // (2 ** Program.combo(combo, input))
        input.instruction += 2
        return input

    @staticmethod
    def bxl(literal: int, input: ProgramInput) -> ProgramInput:
        input.register_b = input.register_b ^ literal
        input.instruction += 2
        return input

    @staticmethod
    def bst(combo: int, input: ProgramInput) -> ProgramInput:
        input.register_b = Program.combo(combo, input) % 8
        input.instruction += 2
        return input

    @staticmethod
    def jnz(literal: int, input: ProgramInput) -> ProgramInput:
        if input.register_a == 0:
            input.instruction += 2
        else:
            input.instruction = literal
        return input

    @staticmethod
    def bxc(_: int, input: ProgramInput) -> ProgramInput:
        input.register_b = input.register_b ^ input.register_c
        input.instruction += 2
        return input

    @staticmethod
    def out(combo: int, input: ProgramInput) -> ProgramInput:
        input.out = str(Program.combo(combo, input) % 8)
        input.instruction += 2
        return input

    @staticmethod
    def bdv(combo: int, input: ProgramInput) -> ProgramInput:
        input.register_b = input.register_a // (2 ** Program.combo(combo, input))
        input.instruction += 2
        return input

    @staticmethod
    def cdv(combo: int, input: ProgramInput) -> ProgramInput:
        input.register_c = input.register_a // (2 ** Program.combo(combo, input))
        input.instruction += 2
        return input
    
    @staticmethod
    def adv_inv(combo: int, out: ProgramInput) -> ProgramInput:
        # if combo is 4, we cannot find the reverse
        if combo == 4:
            raise ValueError
        out.register_a = out.register_a * (2 ** Program.combo(combo, out))
        out.instruction -= 2
        return out

    @staticmethod
    def bxl_inv(literal: int, out: ProgramInput) -> ProgramInput:
        # A XOR B = C -> B = A XOR C
        # XOR inverse says the same
        out.register_b = out.register_b ^ literal
        out.instruction -= 2
        return out

    @staticmethod
    def bst_inv(combo: int, out: ProgramInput) -> ProgramInput:
        # We actually can't reverse this, but we want to minimise the value of
        # register_a at the input, so we'll assume that the value before was zero
        if combo == 4:
            out.register_a = out.register_b * 8
        out.register_b = 0
        out.instruction -= 2
        return out

    @staticmethod
    def jnz_inv(literal: int, input: ProgramInput) -> ProgramInput:
        # This shouldn't be called
        raise NotImplementedError

    @staticmethod
    def bxc_inv(_: int, out: ProgramInput) -> ProgramInput:
        out.register_b = out.register_b ^ out.register_c
        out.instruction -= 2
        return out

    @staticmethod
    def out_inv(combo: int, out: ProgramInput) -> ProgramInput:
        if out.out == "":
            raise ValueError("Out field not set!")
        out_val = int(out.out)
        # Kinda cheating here cuz I just want to cover my test case and actual case
        if combo == 4:
            out.register_a = (out.register_a // 8) * 8 + out_val
        elif combo == 5:
            out.register_b = (out.register_b // 8) * 8 + out_val
        else:
            raise ValueError
        out.instruction -= 2
        return out

    @staticmethod
    def bdv_inv(combo: int, out: ProgramInput) -> ProgramInput:
        out.register_b = 0
        out.instruction -= 2
        return out


    @staticmethod
    def cdv_inv(combo: int, out: ProgramInput) -> ProgramInput:
        if combo == 5:
            out.register_a = out.register_c * (2 ** out.register_b)
        out.register_c = 0
        out.instruction -= 2
        return out


OPCODE: dict[int, Callable[[int, ProgramInput], ProgramInput]] = {
    0: Program.adv,
    1: Program.bxl,
    2: Program.bst,
    3: Program.jnz,
    4: Program.bxc,
    5: Program.out,
    6: Program.bdv,
    7: Program.cdv,
}

OPCODE_INVERSE: dict[int, Callable[[int, ProgramInput], ProgramInput]] = {
    0: Program.adv_inv,
    1: Program.bxl_inv,
    2: Program.bst_inv,
    3: Program.jnz_inv,
    4: Program.bxc_inv,
    5: Program.out_inv,
    6: Program.bdv_inv,
    7: Program.cdv_inv,
}


@cache
def run_program(input: ProgramInput) -> str:
    if input.instruction >= len(input.commands) - 1:
        return ""
    opcode, operand = (
        input.commands[input.instruction],
        input.commands[input.instruction + 1],
    )
    func = OPCODE[opcode]
    next_input = func(operand, input)
    next_move_output = run_program(copy_input(next_input))

    res = []
    if next_input.out:
        res.append(next_input.out)
    if next_move_output:
        res.append(next_move_output)

    return ",".join(res)


def load_data(filename: str) -> Program:
    with open(filename, "r") as f:
        lines = f.readlines()

    a = int(lines[0].strip().split()[-1])
    b = int(lines[1].strip().split()[-1])
    c = int(lines[2].strip().split()[-1])
    commands = lines[4].strip().split()[-1]
    commands = [int(i) for i in commands.split(",")]

    program = Program(a, b, c, commands)
    return program


def solve_part_one(program: Program) -> str:
    input = ProgramInput(program.a, program.b, program.c, 0, program.commands)
    return run_program(input)


def chain(input: ProgramInput, commands: list[int]) -> ProgramInput:
    cur = input
    while cur.instruction < len(commands) - 1:
        opcode, combo = commands[cur.instruction], commands[cur.instruction + 1]
        cur = OPCODE[opcode](combo, cur)
    return cur


def solve_part_two(program: Program) -> int:
    # set up such that it outputs seconds to last, and returns to first
    expected = ",".join([str(c) for c in program.commands])
    # Testcase:
    # a // 8 mod 8
    # Program: 0,3,5,4,3,0
    # in reverse order: 0, 3, 4, 5, 3, 0
    # The program ends in 3, 0, so if a is not zero,
    # it will iterate back to the start.
    # In the last run, a is 0
    # 2nd last: output is 3, start with (3) * 8 = 24, a becomes 3
    # 3rd last: output is 4, start with (24 + 4) * 8 = 224
    # 3th last, output is 5, start with (224 + 5) * 8 = 1832
    # 4th last: output is 3, start with (1832 + 3) * 8 = 12680
    # 5th last: output is 0, start with (15128) * 8 = 117440

    expected = deepcopy(program.commands)
    cur_a = 0
    cur_values: list[int] = []
    input = ProgramInput(0, 0, 0, 0, program.commands)
    while expected:
        cur_expected = expected.pop()
        cur_values.insert(0, cur_expected)
        cur_expected_str = ",".join(str(i) for i in cur_values)
        cur_a = cur_a * 8
        print(cur_a, cur_expected_str)
        for a in range(cur_a, cur_a + 8):
            input = ProgramInput(a, 0, 0, 0, program.commands)
            res = run_program(input)
            print(res)
            if res == cur_expected_str:
                print("FOUND", a, res)
                cur_a = a
                break
        else:
            raise ValueError("Could not find match!")
    return cur_a


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
