import unittest
from part2 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "89010123\n78121874\n87430965\n96549874\n45678903\n32019012\n01329801\n10456732"
        expected_result = 81
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()