from unittest import TestCase

from src.twenty_four.one.main import part_one, part_two
from src.utils import get_input_filename


class TestDayOne(TestCase):
    def setUp(self) -> None:
        self.filename = get_input_filename(__file__)
        return super().setUp()

    def test_part_one(self) -> None:
        expected = 11
        actual = part_one(self.filename)
        self.assertEqual(expected, actual)

    def test_part_two(self) -> None:
        expected = 31
        actual = part_two(self.filename)
        self.assertEqual(expected, actual)
