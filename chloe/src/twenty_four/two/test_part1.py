import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9 10"
        expected_number_of_safe_reports = 2
        
        number_of_safe_reports = main(input_string)
        
        self.assertEqual(number_of_safe_reports, expected_number_of_safe_reports)

if __name__ == '__main__':
    unittest.main()