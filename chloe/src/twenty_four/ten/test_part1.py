import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_1(self):
        input_string = "0123\n1234\n8765\n9876"
        expected_result = 1
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)
    
    
    def test_2(self):
        input_string = "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"
        expected_result = 36
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()