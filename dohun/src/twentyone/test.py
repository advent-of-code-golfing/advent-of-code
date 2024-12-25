from config import KEYPAD_1, KEYPAD1_LOC, KEYPAD_2, KEYPAD2_LOC, DIRECTIONS_DICT
from main import Robot


def keypad_test():
    for LOC, KEYPAD in zip([KEYPAD1_LOC, KEYPAD2_LOC], [KEYPAD_1, KEYPAD_2]):
        for symbol, loc in LOC.items():
            assert KEYPAD[loc[0]][loc[1]] == symbol
    print("all assertions passed")


def test_evaluation_and_inversion() -> None:
    robot_1 = Robot(KEYPAD_1, KEYPAD1_LOC)
    assert "029A" == robot_1.evaluate_commands("<A^A>^^AvvvA")
    assert len("<A^A>^^AvvvA") == len(robot_1.invert_commands("029A"))
    assert robot_1.test_inversion("029A")

    robot_2 = Robot(KEYPAD_2, KEYPAD2_LOC)
    assert "<A^A>^^AvvvA" == robot_2.evaluate_commands("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")
    assert len("v<<A>>^A<A>AvA<^AA>A<vAAA>^A") == len(
        robot_2.invert_commands("<A^A>^^AvvvA")
    )
    assert robot_2.test_inversion("<A^A>^^AvvvA")

    robot_3 = Robot(KEYPAD_2, KEYPAD2_LOC)
    assert "v<<A>>^A<A>AvA<^AA>A<vAAA>^A" == robot_3.evaluate_commands(
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    )
    assert len(
        "<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A"
    ) == len(robot_2.invert_commands("v<<A>>^A<A>AvA<^AA>A<vAAA>^A"))
    assert robot_2.test_inversion("v<<A>>^A<A>AvA<^AA>A<vAAA>^A")

    print("all evaluation and inversion tests have passed")


if __name__ == "__main__":
    keypad_test()
    test_evaluation_and_inversion()
