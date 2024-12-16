import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main(self):
        input_string = "AAAA\nBBCD\nBBCC\nEEEC"
        expected_result = 140
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

    def test_main_2(self):
        input_string = "OOOOO\nOXOXO\nOOOOO\nOXOXO\nOOOOO"
        expected_result = 772
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

    def test_main_3(self):
        input_string = "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"
        expected_result = 1930
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()