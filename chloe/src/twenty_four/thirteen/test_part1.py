import unittest
from part1 import main

class TestMain(unittest.TestCase):
    
    def test_main(self):
        input_string = "Button A: X+94, Y+34\nButton B: X+22, Y+67\nPrize: X=8400, Y=5400\n\nButton A: X+26, Y+66\nButton B: X+67, Y+21\nPrize: X=12748, Y=12176\n\nButton A: X+17, Y+86\nButton B: X+84, Y+37\nPrize: X=7870, Y=6450\n\nButton A: X+69, Y+23\nButton B: X+27, Y+71\nPrize: X=18641, Y=10279"
        expected_result = 480
        
        result = main(input_string)
        
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()