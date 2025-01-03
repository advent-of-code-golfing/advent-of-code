KEYPAD_1 = [["7", "8", "9"], ["4", "5", "6"], ["1", "2", "3"], ["NO_GO", "0", "A"]]

KEYPAD1_LOC = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
    "NO_GO": (3, 0),
}

KEYPAD_2 = [["NO_GO", "^", "A"], ["<", "v", ">"]]

KEYPAD2_LOC = {
    "NO_GO": (0, 0),
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

DIRECTIONS_DICT = {"^": (-1, 0), ">": (0, 1), "<": (0, -1), "v": (1, 0)}