from src.utils import get_input_filename
from collections import Counter

import numpy as np 
import copy


def load_data(filename: str) -> tuple:
    map = []
    with open(filename, "r") as f:
        for line in f.readlines(): 
            line_raw = line.strip('\n')
            line_list = []
            for char in line_raw: 
                if char == '.': 
                    line_list.append(0)
                elif char == '#': 
                    line_list.append(1)
                else: 
                    line_list.append(2) 

            map.append(line_list)            
        return np.array(map), 'N'


ROTATION_MAP: {
    'N': 'E', 
    'E': 'S', 
    'S': 'W', 
    'W': 'N'
}


def _guard_one_iteration(map: np.array, 
                         guard_loc: tuple, 
                         direction: str, 
                         guard_tracker_map: np.array
                         ) -> tuple: 

    loc_i, loc_j = guard_loc
    if direction == 'N': 
        hurdle = map[:loc_i, loc_j]
    elif direction == 'E': 
        hurdle = map[loc_i, loc_j+1:]
    elif direction == 'S': 
        hurdle = map[loc_i+1:, loc_j]
    else: 
        hurdle = map[loc_i, :loc_j]
    
    hurdle_exists = np.sum(hurdle==1)

    if not hurdle_exists: 
        if direction == 'N': 
            guard_tracker_map[:loc_i, loc_j] = 3
        elif direction == 'E': 
            guard_tracker_map[loc_i, loc_j+1:] = 3
        elif direction == 'S': 
            guard_tracker_map[loc_i+1:, loc_j] = 3
        else: 
            guard_tracker_map[loc_i, :loc_j] = 3
    
        return map, direction, len(hurdle), guard_tracker_map


    if direction == 'N': 
        first_hurdle = int(np.where(hurdle == 1)[0][-1])
        hurdle_tracker = guard_tracker_map[:loc_i, loc_j]
        hurdle_tracker[first_hurdle+1:] = 3
        hurdle[first_hurdle + 1] = 2
        map[:loc_i, loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[first_hurdle+1:])
        guard_tracker_map[:loc_i, loc_j] = hurdle_tracker.copy()

        return map, 'E', dist_travelled, guard_tracker_map


    if direction == 'E': 
        first_hurdle = int(np.where(hurdle == 1)[0][0])
        hurdle_tracker = guard_tracker_map[loc_i, loc_j+1:]
        hurdle_tracker[:first_hurdle] = 3
        hurdle[first_hurdle - 1] = 2
        map[loc_i, loc_j+1:] = hurdle.copy()
        dist_travelled = len(hurdle[:first_hurdle])
        guard_tracker_map[loc_i, loc_j+1:] = hurdle_tracker.copy()

        return map, 'S', dist_travelled, guard_tracker_map


    if direction == 'S': 
        first_hurdle = int(np.where(hurdle == 1)[0][0])
        hurdle_tracker = guard_tracker_map[loc_i+1:, loc_j]
        hurdle_tracker[:first_hurdle] = 3
        hurdle[first_hurdle - 1] = 2
        map[loc_i+1:, loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[:first_hurdle])
        guard_tracker_map[loc_i+1:, loc_j] = hurdle_tracker.copy()

        return map, 'W', dist_travelled, guard_tracker_map


    if direction == 'W': 
        first_hurdle = int(np.where(hurdle == 1)[0][-1])
        hurdle_tracker = guard_tracker_map[loc_i, :loc_j]
        hurdle_tracker[first_hurdle+1:] = 3
        hurdle[first_hurdle + 1] = 2
        map[loc_i, :loc_j] = hurdle.copy()
        dist_travelled = len(hurdle[first_hurdle+1:])
        guard_tracker_map[loc_i, :loc_j] = hurdle_tracker.copy()

        return map, 'N', dist_travelled, guard_tracker_map


def q1(map: np.array, direction: str) -> int:
    guard_exists = np.sum(map==2) 
    guard_tracker_map = map.copy()

    while guard_exists: 
        loc_i, loc_j = (int(x) for x in np.where(map==2))
        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3
        
        map, direction, dist_travelled, guard_tracker_map = _guard_one_iteration(map, (loc_i, loc_j), direction, guard_tracker_map)
        guard_exists = np.sum(map==2) 

    return np.sum(guard_tracker_map == 3) 


def q2(map: np.array, direction: str) -> int: 
    guard_exists = np.sum(map==2) 
    guard_tracker_map = map.copy()

    previous_stops = dict()
    #Run once to see the potential places we can place an obstruction
    while guard_exists: 
        loc_i, loc_j = (int(x) for x in np.where(map==2))
        previous_stops[loc_i, loc_j] = direction
        map[loc_i, loc_j] = 0
        guard_tracker_map[loc_i, loc_j] = 3
        
        map, direction, dist_travelled, guard_tracker_map = _guard_one_iteration(map, (loc_i, loc_j), direction, guard_tracker_map)
        guard_exists = np.sum(map==2) 

    return np.sum(guard_tracker_map == 3) 




if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    map, direction = load_data(filename)
    print(q1(map, direction))
    print(q2(map, direction))

