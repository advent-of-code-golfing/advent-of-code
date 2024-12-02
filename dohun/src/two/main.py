from src.utils import get_input_filename
import numpy as np 


def load_data(filename: str) -> tuple[list[int], list[int]]:
    input_list: list[int] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            nums = line.strip().split()
            input_list.append([int(l) for l in nums])
            
    return input_list


def q1(input_list: list) -> int:
    count = 0
    for input in input_list: 
        len_input = len(input)
        prev_diff = None
        for i in range(len_input): 
            if i == len_input - 1: 
                count += 1
                print(count)
                print(input)
                print('\n')
                continue
            diff = input[i+1] - input[i]
            if abs(diff) >= 1 and abs(diff) <=3: 
                if prev_diff is None: 
                    prev_diff = diff
                    continue
                if prev_diff * diff > 0: 
                    prev_diff = diff
                    continue
                else: 
                    break
            else: 
                break
                
    return count 


def q2(input_list: list) -> int: 

    
    return 0


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    input_list = load_data(filename)
    print(q1(input_list))
    print(q2(input_list))