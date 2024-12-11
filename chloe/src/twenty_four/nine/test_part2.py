import unittest
from part2 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "2333133121414131402"
        expected_result = 2858
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()