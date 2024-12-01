from unittest import TestCase

from kyubin.src.twenty_four.one.main import part_one, part_two


class TestDayOne(TestCase):
    def setUp(self) -> None:
        self.left = [3, 4, 2, 1, 3, 3]
        self.right = [4, 3, 5, 3, 9, 3]
        return super().setUp()

    def test_part_one(self) -> None:
        expected = 11
        actual = part_one(self.left, self.right)
        self.assertEqual(expected, actual)

    def test_part_two(self) -> None:
        expected = 31
        actual = part_two(self.left, self.right)
        self.assertEqual(expected, actual)
