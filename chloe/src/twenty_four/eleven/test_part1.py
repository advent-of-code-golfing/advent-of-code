import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main(self):
        input_string = "125 17"
        expected_result = 55312
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()