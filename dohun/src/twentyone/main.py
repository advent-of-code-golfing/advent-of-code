from src.utils import get_input_filename
from collections import Counter
import itertools
from functools import cache

import numpy as np
import copy

from config import KEYPAD_1, KEYPAD1_LOC, KEYPAD_2, KEYPAD2_LOC, DIRECTIONS_DICT


def load_data(is_test: bool = True) -> list:
    req_com_list = ["539A", "964A", "803A", "149A", "789A"]
    if is_test:
        req_com_list = ["029A", "980A", "179A", "456A", "379A"]

    return req_com_list


class Robot:
    def __init__(self, keypad: list[list], keypad_loc: dict):
        self.keypad = keypad
        self.keypad_loc = keypad_loc
        self.num_rows = len(keypad)
        self.num_cols = len(keypad[0])
        self._initialize_current_loc()

    def _initialize_current_loc(self) -> None:
        self.current_loc = self.keypad_loc["A"]

    def call_keypad(self, loc: tuple) -> str:
        return self.keypad[loc[0]][loc[1]]

    def _check_inrange(self, loc: tuple) -> bool:
        row_loc, col_loc = loc
        row_in_range = 0 <= row_loc < self.num_rows
        col_in_range = 0 <= col_loc < self.num_cols

        return row_in_range and col_in_range

    def _move(self, loc: tuple, dir: str) -> tuple:
        dir_coord = DIRECTIONS_DICT[dir]
        return loc[0] + dir_coord[0], loc[1] + dir_coord[1]

    def _move_current_loc(self, dir: str) -> None:
        new_loc = self._move(self.current_loc, dir)
        if self._check_inrange(new_loc):
            self.current_loc = new_loc

    def evaluate_commands(self, command_str: str) -> str:
        output_str = ""
        for command in command_str:
            if command == "A":
                output_str = output_str + self.call_keypad(self.current_loc)
            else:
                self._move_current_loc(command)

        self._initialize_current_loc()

        return output_str

    def calculate_dist_vect(self, loc_1: tuple, loc_2: tuple) -> tuple:
        return loc_2[0] - loc_1[0], loc_2[1] - loc_1[1]

    def get_op_str(self, row_op: int, col_op: int) -> tuple:
        row_op_str = "^"
        if row_op > 0:
            row_op_str = "v"

        col_op_str = "<"
        if col_op > 0:
            col_op_str = ">"
        return row_op_str, col_op_str

    def _check_nogo(self, op: int, op_str: str):
        new_loc = copy.copy(self.current_loc)
        for _ in range(abs(op)):
            new_loc = self._move(new_loc, op_str)
            if self.call_keypad(new_loc) == "NO_GO":
                return True

        return False

    def append_to_command_str(self, command_str, row_op: int, col_op: int):
        row_op_str, col_op_str = self.get_op_str(row_op, col_op)
        preferred_order = [(col_op, col_op_str), (row_op, row_op_str)]
        preferred_order_reverse = [(row_op, row_op_str), (col_op, col_op_str)]

        if col_op_str == ">":
            preferred_order, preferred_order_reverse = (
                preferred_order_reverse,
                preferred_order,
            )

        if self._check_nogo(preferred_order[0][0], preferred_order[0][1]):
            preferred_order, preferred_order_reverse = (
                preferred_order_reverse,
                preferred_order,
            )

        for op, op_str in preferred_order:
            for _ in range(abs(op)):
                command_str = command_str + op_str

        return command_str

    def invert_commands(self, required_str: str):
        command_str = ""
        for next_needed in required_str:
            next_loc = self.keypad_loc[next_needed]
            row_op, col_op = self.calculate_dist_vect(self.current_loc, next_loc)
            # Need to deal with robot going over the gap
            command_str = self.append_to_command_str(command_str, row_op, col_op)
            self.current_loc = next_loc
            assert self.call_keypad(self.current_loc) == next_needed
            command_str = command_str + "A"

        self._initialize_current_loc()

        return command_str

    def test_inversion(self, required_str: str):
        command_str = self.invert_commands(required_str)
        return self.evaluate_commands(command_str) == required_str

    @cache
    def one_step_inverted(self, start_str: str, end_str: str) -> dict:
        current_loc = self.keypad_loc[start_str]
        self.current_loc = current_loc
        command_str = self.invert_commands(end_str)

        return decompose_string(command_str)


def decompose_string(command_str: str) -> dict:
    str_len = len(command_str)

    decom_str_dict = dict()
    first_req = "A", command_str[0]
    decom_str_dict[first_req] = 1

    for i in range(1, str_len):
        req = command_str[i - 1], command_str[i]
        if req in decom_str_dict:
            decom_str_dict[req] += 1
        else:
            decom_str_dict[req] = 1

    return decom_str_dict


def q1(req_com_list: list) -> int:
    robot_1 = Robot(KEYPAD_1, KEYPAD1_LOC)
    robot_2 = Robot(KEYPAD_2, KEYPAD2_LOC)
    robot_3 = Robot(KEYPAD_2, KEYPAD2_LOC)

    complexity = 0
    for req_command in req_com_list:
        req_req_command = robot_1.invert_commands(req_command)
        req_req_req_command = robot_2.invert_commands(req_req_command)
        req_req_req_req_command = robot_3.invert_commands(req_req_req_command)

        numeric = int(req_command[0:3])
        len_seq = len(req_req_req_req_command)
        complexity += numeric * len_seq

    return complexity


def q2(req_com_list: list, num_inv_req: int = 2) -> int:
    robot_1 = Robot(KEYPAD_1, KEYPAD1_LOC)
    robot_2 = Robot(KEYPAD_2, KEYPAD2_LOC)

    complexity = 0
    for req_command in req_com_list:
        req_req_command = robot_1.invert_commands(req_command)
        req_str_decomposed_dict = decompose_string(req_req_command)

        for _ in range(num_inv_req):
            new_req_str_decomposed_dict = dict()
            for key, value in req_str_decomposed_dict.items():
                inversion_dict = robot_2.one_step_inverted(key[0], key[1])
                for new_key, new_value in inversion_dict.items():
                    if new_key in new_req_str_decomposed_dict:
                        new_req_str_decomposed_dict[new_key] += new_value * value
                    else:
                        new_req_str_decomposed_dict[new_key] = new_value * value
            req_str_decomposed_dict = new_req_str_decomposed_dict

        numeric = int(req_command[0:3])
        len_seq = sum([x for x in req_str_decomposed_dict.values()])
        complexity += numeric * len_seq

    return complexity


if __name__ == "__main__":
    req_com_list = load_data(is_test=False)
    print(q1(req_com_list))
    print(q2(req_com_list, num_inv_req=25))
