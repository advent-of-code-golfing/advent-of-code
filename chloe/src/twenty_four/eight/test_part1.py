import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "............\n........0...\n.....0......\n.......0....\n....0.......\n......A.....\n............\n............\n........A...\n.........A..\n............\n............"
        expected_result = 14
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()