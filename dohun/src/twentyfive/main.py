from src.utils import get_input_filename
import numpy as np
import copy


def load_data(filename: str) -> tuple:
    keys_space_list = list()

    key_space = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                keys_space_list += [np.array(copy.deepcopy(key_space))]
                key_space = list()
            else: 
                line_num = list()
                for str in line: 
                    if str == '#': 
                        line_num.append(1)
                    else: 
                        line_num.append(0)
                key_space.append(line_num)
    
    locks_list = list()
    keys_list = list()
    
    for key_space in keys_space_list: 
        assert((key_space[0] == 0).all() and (key_space[-1] == 1).all() or 
               (key_space[0] == 1).all() and (key_space[-1] == 0).all())

        if (key_space[0] == 1).all() and (key_space[-1] == 0).all(): 
            locks_list.append(key_space)
        else: 
            keys_list.append(key_space)
    return locks_list, keys_list


def q1(locks_list: list, keys_list: list) -> int:
    num_comb = 0
    for lock in locks_list: 
        for key in keys_list: 
            check = lock + key    
            if (check <= 1).all(): 
                num_comb += 1
    return num_comb


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    locks_list, keys_list = load_data(filename)
    print(q1(locks_list, keys_list))
