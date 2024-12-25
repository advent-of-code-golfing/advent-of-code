from src.utils import get_input_filename
from collections import Counter
import itertools

import numpy as np
import copy
import re


def extract_numbers_from_block(text_block: str) -> tuple:
    # Use regex to find all numbers after '+' or '='
    numbers = re.findall(r"\+(\d+)|=(\d+)", text_block)
    # Flatten the list of tuples and remove None values
    extracted_numbers = [
        int(num) for tuple_item in numbers for num in tuple_item if num
    ]

    eq = np.array(
        [
            [extracted_numbers[0], extracted_numbers[2]],
            [extracted_numbers[1], extracted_numbers[3]],
        ]
    )
    sol = np.array([extracted_numbers[4], extracted_numbers[5]])

    return eq, sol


def load_data(filename: str) -> list:
    sol_vectors = list()
    eq_vectors = list()
    with open(filename, "r") as f:
        text = f.read()
        blocks = [block.strip() for block in text.split("\n\n") if block.strip()]

        block_nums = [extract_numbers_from_block(block) for block in blocks]

    for eq, sol in block_nums:
        sol_vectors.append(sol)
        eq_vectors.append(eq)

    return sol_vectors, eq_vectors


def _price_if_exists(
    sol_vector: np.array, eq_vector: np.array, care_about_inrange: bool = True
) -> int:
    a, b, c, d = eq_vector[0, 0], eq_vector[0, 1], eq_vector[1, 0], eq_vector[1, 1]
    det = a * d - b * c
    if det != 0:
        # I think I have a numerical issue so try solve it directly
        # matrix looks like
        # a b
        # c d
        # and solution vector like
        # e
        # f
        # presses = np.matmul(np.linalg.inv(eq_vector), sol_vector)
        # a_presses, b_presses = round(presses[0], 4), round(presses[1], 4)
        # is_integer = a_presses.is_integer() and b_presses.is_integer()
        # we want X^-1 Y
        # so
        # 1 / * d  -b * e   = 1 /   de - bf
        # det  -c   a   f      det  -ce + af
        e, f = sol_vector[0], sol_vector[1]

        top = d * e - b * f
        bottom = -c * e + a * f

        is_integer = ((top % det) == 0) and ((bottom % det) == 0)
        if is_integer:
            a_presses = top / det
            b_presses = bottom / det

            if care_about_inrange:
                is_inrange = (0 <= a_presses <= 100) and (0 <= b_presses <= 100)
            else:
                is_inrange = (0 <= a_presses) and (0 <= b_presses)

            if is_inrange:
                return a_presses * 3 + b_presses

        return 0
    else:
        if all(sol_vector / eq_vector[:, 0]):
            a_attempt = (sol_vector / eq_vector[:, 0])[0]
            b_attempt = (sol_vector / eq_vector[:, 1])[0]

            if a_attempt.is_integer() and not b_attempt.is_integer():
                return 3 * a_attempt
            elif not a_attempt.is_integer() and b_attempt.is_integer():
                return b_attempt
            elif a_attempt.is_integer() and b_attempt.is_integer():
                return min(3 * a_attempt, b_attempt)
            else:
                return 0
        else:
            return 0


def q1(sol_vectors: list, eq_vectors: list) -> int:
    price = 0
    for sol_vector, eq_vector in zip(sol_vectors, eq_vectors):
        price += _price_if_exists(sol_vector, eq_vector)

    return price


def q2(sol_vectors: list, eq_vectors: list) -> int:
    price = 0
    i = 0
    for sol_vector, eq_vector in zip(sol_vectors, eq_vectors):
        sol_vector = sol_vector + np.array([10000000000000, 10000000000000])
        price += _price_if_exists(sol_vector, eq_vector, care_about_inrange=False)

    return price


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    sol_vectors, eq_vectors = load_data(filename)
    print(q1(sol_vectors, eq_vectors))
    print(q2(sol_vectors, eq_vectors))
