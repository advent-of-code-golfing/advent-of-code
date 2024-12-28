from src.utils import get_input_filename
import time
import copy


def load_data(filename: str) -> tuple:
    known_dict = dict()
    to_calc_list = list()
    to_calc_dict = dict()
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
                to_calc_dict[parts[3]] = {'values': [parts[0], parts[2]], 'operation': parts[1]}

    return known_dict, to_calc_list, to_calc_dict


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


def calculate_output(known_dict: dict, var_to_calc: str = 'z') -> int: 
    z_wires = [wire for wire in known_dict if wire.startswith(var_to_calc)]
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


def addition_test(to_calc_list: list) -> list: 
    fails = list()
    for i in range(45): 
        # for test in ['test1', 'test2', 'test3']
        known_dict = dict()
        for j in range(45): 
            if j < 10: 
                known_dict['x' + '0' + str(j)] = 0
                known_dict['y' + '0' + str(j)] = 0
            else: 
                known_dict['x' + str(j)] = 0
                known_dict['y' + str(j)] = 0
        if i < 10: 
            known_dict['x' + '0' + str(i)] = 1
            known_dict['y' + '0' + str(i)] = 1
        else: 
            known_dict['x' + str(i)] = 1
            known_dict['y' + str(i)] = 1
        
        x = calculate_output(known_dict, 'x')
        y = calculate_output(known_dict, 'y')
        z = q1(copy.deepcopy(known_dict), copy.deepcopy(to_calc_list))

        if x+y != z: 
            fails.append(i)
            print(f'addition test failed for {i}')

    if len(fails) == 0: 
        print('addition test passed')
        print('--------------------')
    else: 
        print('addition test failed')
        print('--------------------')
    return fails 

def get_all_dependencies(val: int, to_calc_dict: dict) -> list: 
    deps = list()
    first_level = to_calc_dict[val]['values'] 

    for dep in first_level: 
        deps.append(dep)
        if not(dep.startswith('x') or dep.startswith('y')): 
            deps += get_all_dependencies(dep, to_calc_dict)
    
    deps = list(set(deps))
    deps.sort()
    return deps 


def find_needed_deps(z: str) -> list: 
    z_num = int(z[1:]) 

    needed_deps_list = list()
    for i in range(z_num+1):
        if i < 10: 
            needed_deps_list.append('x' + '0' + str(i))
            needed_deps_list.append('y' + '0' + str(i))
        else: 
            needed_deps_list.append('x' + str(i))
            needed_deps_list.append('y' + str(i))
    
    needed_deps_list.sort()
    return needed_deps_list  


def make_swaps(swap_list: list, to_calc_list: list) -> list: 
    for swap in swap_list: 
        locs = list()
        for i, to_calc in enumerate(to_calc_list): 
            if to_calc[3] in swap: 
                locs.append(i)
        assert(len(locs) == len(swap))

        if to_calc_list[locs[0]][3] == swap[0]: 
            to_calc_list[locs[0]][3], to_calc_list[locs[1]][3] = swap[1], swap[0]
        else: 
            to_calc_list[locs[0]][3], to_calc_list[locs[1]][3] = swap[0], swap[1]

    return to_calc_list 


def q2_attempt(to_calc_list: list, 
               to_calc_dict: dict) -> None: 
    '''
    Saving some failed attempts for this question, mostly searching for dependencies on the levels below
    '''
    xy_AND_dict = dict()
    xy_OR_dict = dict()
    for to_calc in to_calc_list: 
        if (to_calc[0].startswith('x') and to_calc[2].startswith('y')) or (to_calc[0].startswith('y') and to_calc[2].startswith('x')): 
            assert(int(to_calc[0][1:]) == int(to_calc[2][1:]))
            num = int(to_calc[0][1:])
            if to_calc[1] == 'XOR': 
                xy_OR_dict[num] = to_calc[3]
            else: 
                xy_AND_dict[num] = to_calc[3]

    dependencies_dict = dict()
    for gate in to_calc_dict.keys(): 
        dependencies_dict[gate] = get_all_dependencies(gate, to_calc_dict=to_calc_dict)
    
    z_list = [x for x in to_calc_dict.keys() if x.startswith('z')]
    
    wrong_deps_2 = list()
    for z in z_list: 
        num = int(z[1:])
        if num in xy_OR_dict: 
            if xy_OR_dict[num] not in dependencies_dict[z]: 
                wrong_deps_2.append(z)
        if num > 0 and xy_AND_dict[num-1] not in dependencies_dict[z]: 
            wrong_deps_2.append(z)

    current_deps = dict()
    wrong_deps = dict()
    for z in z_list: 
        if z == 'z45': 
            continue
        needed_deps = find_needed_deps(z)
        if needed_deps != dependencies_dict[z]: 
            diff1 = list(set(needed_deps) - set(dependencies_dict[z]))   
            diff2 = list(set(dependencies_dict[z]) - set(needed_deps))   
            wrong_deps[z] = diff1 
            current_deps[z] = diff2
    
    potential = list()
    for _, missing_deps in wrong_deps.items(): 
        for gate, gate_dep in dependencies_dict.items(): 
            if set(gate_dep) <= set(missing_deps): 
                potential.append(gate)


def q2(to_calc_list: list, 
    ) -> str:
    '''
    In the end most of the answers I found analyitically, by finding the failing test cases and going through the logic
    (each z has to have a dependencies on XOR of its level and AND on the level below). This problem definitely could have
    been much harder, as most of the cases are quite easily findable analytically. Would be quite interested to see what
    other computational solutions are available
    '''
    addition_test(copy.deepcopy(to_calc_list))
    swap_list = [['z16', 'hmk'], ['z33', 'fcd'], ['fhp', 'z20'], ['rvf', 'tpc']]
    new_to_calc_list = make_swaps(swap_list=swap_list, 
                                  to_calc_list=copy.deepcopy(to_calc_list))
    addition_test(copy.deepcopy(new_to_calc_list))

    swaps_flattened = ['z16', 'hmk', 'z33', 'fcd', 'fhp', 'z20', 'rvf', 'tpc']
    swaps_flattened.sort()

    return ','.join(swaps_flattened)


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    known_dict, to_calc_list, _ = load_data(filename)
    print(q1(known_dict, to_calc_list))
    known_dict, to_calc_list, to_calc_dict = load_data(filename)
    print(q2(to_calc_list))
