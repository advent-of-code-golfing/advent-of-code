import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "190: 10 19\n3267: 81 40 27\n83: 17 5\n156: 15 6\n7290: 6 8 6 15\n161011: 16 10 13\n192: 17 8 14\n21037: 9 7 18 13\n292: 11 6 16 20"

        expected_result = 3749
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()