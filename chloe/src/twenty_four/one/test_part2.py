import unittest
from part2 import main

class TestMain(unittest.TestCase):
    
    def test_main_small(self):
        input_string = "3 4\n4 3\n2 5\n1 3\n3 9\n3 3"
        expected_similarity_score = 31
        
        similarity_score = main(input_string)
        
        self.assertEqual(similarity_score, expected_similarity_score)

if __name__ == '__main__':
    unittest.main()