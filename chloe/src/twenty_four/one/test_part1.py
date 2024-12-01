import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "5 4\n3 2\n1 6"
        expected_difference = 3
        
        difference = main(input_string)
        
        self.assertEqual(difference, expected_difference)

    def test_main_large(self):
        input_string = "123 456\n789 101112\n131415 161718\n23 2434"
        expected_difference = (456 - 23) + (2434 - 789) + (101112 - 123) + (161718-131415)

        difference = main(input_string)

        self.assertEqual(difference, expected_difference)

if __name__ == '__main__':
    unittest.main()