import unittest
from part2 import main

class TestMain(unittest.TestCase):
    
    def test_main(self):
        input_string = "AAAA\nBBCD\nBBCC\nEEEC"
        expected_result = 80
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

    def test_main_2(self):
        input_string = "EEEEE\nEXXXX\nEEEEE\nEXXXX\nEEEEE"
        expected_result = 236
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

    def test_main_3(self):
        input_string = "AAAAAA\nAAABBA\nAAABBA\nABBAAA\nABBAAA\nAAAAAA"
        expected_result = 368
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

    def test_main_4(self):
        input_string = "RRRRIICCFF\nRRRRIICCCF\nVVRRRCCFFF\nVVRCCCJFFF\nVVVVCJJCFE\nVVIVCCJJEE\nVVIIICJJEE\nMIIIIIJJEE\nMIIISIJEEE\nMMMISSJEEE"
        expected_result = 1206
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()