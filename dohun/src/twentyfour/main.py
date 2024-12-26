from src.utils import get_input_filename


def load_data(filename: str) -> tuple:
    known_dict = dict()
    to_calc_list = list()
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == '\n' or line == '': 
                continue 
            if ':' in line: 
                wire, wire_val = line.split(': ')
                assert (wire not in known_dict)
                known_dict[wire] = int(wire_val)
            else: 
                line = line.replace('-> ', '')
                parts = line.split(' ')
                assert (len(parts) == 4)
                to_calc_list.append(parts)

    return known_dict, to_calc_list


def can_calculate(to_calc: list, known_dict: dict) -> bool: 
    if to_calc[0] in known_dict and to_calc[2] in known_dict: 
        return True
    return False


def calculate(val_1: int, val_2: int, op: str): 
    assert(op in ('XOR', 'OR', 'AND'))

    if op == 'XOR': 
        if val_1 != val_2: 
            return True
        return False
    elif op == 'OR': 
        return val_1 or val_2
    else: 
        return val_1 and val_2


def calculate_output(known_dict: dict) -> int: 
    z_wires = [wire for wire in known_dict if wire.startswith('z')]
    output = 0
    for z_wire in z_wires: 
        calc_value = known_dict[z_wire]
        power = int(z_wire[1:])
        output += calc_value * 2**power
    
    return output 

def q1(
    known_dict: dict,
    to_calc_list: list
) -> int:
    calc_needed = len(to_calc_list)
    while calc_needed > 0: 
        can_calculate_list = list()
        for to_calc in to_calc_list: 
            if can_calculate(to_calc, known_dict): 
                can_calculate_list.append(to_calc)
        
        for can_calc in can_calculate_list: 
            assert(can_calc[3] not in known_dict)
            known_dict[can_calc[3]] = calculate(known_dict[can_calc[0]], 
                                                known_dict[can_calc[2]], 
                                                can_calc[1])
            to_calc_list.remove(can_calc)
        calc_needed = len(to_calc_list)
    
    return calculate_output(known_dict=known_dict)


def q2(known_dict: dict, 
       to_calc_list: list) -> int:
    print('hello')    
    return 0


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    known_dict, to_calc_list = load_data(filename)
    print(q1(known_dict, to_calc_list))
    print(q2(known_dict, to_calc_list))
