from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy


class Device:
    def __init__(
        self,
        Reg_A: int = None,
        Reg_B: int = None,
        Reg_C: int = None,
        Program: list = [],
    ):
        self.Reg_A = Reg_A
        self.Reg_B = Reg_B
        self.Reg_C = Reg_C
        self.Program = Program
        self.output = []
        self._reevaluate_com_op()

    def _reevaluate_com_op(self):
        self.com_op = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.Reg_A,
            5: self.Reg_B,
            6: self.Reg_C,
            7: None,
        }

    def display(self):
        print("--------------")
        print("Register A is: ", self.Reg_A)
        print("Register B is: ", self.Reg_B)
        print("Register C is: ", self.Reg_C)
        print("Output is: ", self.output)
        print("--------------")

    def run(self):
        assert len(self.Program) % 2 == 0

        k = 0
        while k < len(self.Program):
            opcode = self.Program[k]
            lit_op = self.Program[k + 1]
            com_op = self.com_op[lit_op]
            if opcode != 3:
                self._run_instructions(opcode, lit_op, com_op)

            if opcode == 3:
                if self.Reg_A == 0:
                    k = k + 2
                    continue
                else:
                    k = lit_op
                    continue
            k = k + 2

    def _run_instructions(self, opcode: int, lit_op: int, com_op: int):
        if opcode == 0:
            num = self.Reg_A
            denom = 2**com_op
            result = num // denom
            self.Reg_A = result
        if opcode == 1:
            self.Reg_B = self.Reg_B ^ lit_op
        if opcode == 2:
            self.Reg_B = com_op % 8
        if opcode == 4:
            self.Reg_B = self.Reg_B ^ self.Reg_C
        if opcode == 5:
            self.output.append(com_op % 8)
        if opcode == 6:
            num = self.Reg_A
            denom = 2**com_op
            result = num // denom
            self.Reg_B = result
        if opcode == 7:
            num = self.Reg_A
            denom = 2**com_op
            result = num // denom
            self.Reg_C = result
        self._reevaluate_com_op()


def load_data(example: str) -> Device:
    if example == "example_1":
        device = Device(Reg_C=9, Program=[2, 6])
    elif example == "example_2":
        device = Device(Reg_A=10, Program=[5, 0, 5, 1, 5, 4])
    elif example == "example_3":
        device = Device(Reg_A=2024, Program=[0, 1, 5, 4, 3, 0])
    elif example == "example_4":
        device = Device(Reg_B=29, Program=[1, 7])
    elif example == "example_5":
        device = Device(Reg_B=2024, Reg_C=43690, Program=[4, 0])
    elif example == "example_6":
        device = Device(Reg_A=729, Reg_B=0, Reg_C=0, Program=[0, 1, 5, 4, 3, 0])
    elif example == "checking_to_be_sure":
        device = Device(
            Reg_A=202367025818154,
            Reg_B=0,
            Reg_C=0,
            Program=[2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0],
        )
    else:
        device = Device(
            Reg_A=30553366,
            Reg_B=0,
            Reg_C=0,
            Program=[2, 4, 1, 1, 7, 5, 4, 7, 1, 4, 0, 3, 5, 5, 3, 0],
        )
    return device


def q1(
    device: list,
):
    device.run()
    device.display()
    return 0


def req_func_simp(Reg_A) -> list:
    output = []
    while Reg_A != 0:
        mid_B = (Reg_A % 8) ^ 1
        Reg_B = (mid_B ^ (Reg_A // 2**mid_B)) ^ 4

        output.append(Reg_B % 8)
        Reg_A = Reg_A // 8

    return output


def q2(
    device: list,
) -> int:
    required_output = device.Program
    len_required_output = len(required_output)

    Reg_A_starts = [0]
    for i in range(len_required_output):
        current_required_output = required_output[len_required_output - i - 1 :]

        new_Reg_A_starts = []
        for Reg_A_start in Reg_A_starts:
            min_Reg_A = max(Reg_A_start * 8, 1)
            max_Reg_A = Reg_A_start * 8 + 7
            for Reg_A_check in range(min_Reg_A, max_Reg_A + 1):
                temp_output = req_func_simp(Reg_A_check)
                if temp_output[0] == current_required_output[0]:
                    new_Reg_A_starts.append(Reg_A_check)

        Reg_A_starts = new_Reg_A_starts

    return min(Reg_A_starts)


if __name__ == "__main__":
    device = load_data("checking_to_be_sure")
    print(q1(device))
    device = load_data("realshit")
    print(q2(device))
