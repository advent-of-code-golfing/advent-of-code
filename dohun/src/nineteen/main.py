from src.utils import get_input_filename
from collections import Counter
import itertools
from functools import cache 
import numpy as np 
import copy
from pathlib import Path
from time import time 


def load_data(filename: str) -> tuple:
    towels_list = list()
    target_towels = list()
    with open(filename, "r") as f:
        for line in f.readlines(): 
            if line == '\n': 
                continue 
            if ',' not in line: 
                target_towels.append(line.strip())

            line = line.strip().split(', ')
            if len(line) > 1: 
                towels_list += line
    
    towels_dict = {x:True for x in towels_list}
    return towels_dict, target_towels


#Bit grim, but need a global variable to make caching work. Maybe better to use frozendict? 
towels_list = list()
dir = Path(__file__).parent / "input.txt"
with open(dir.__str__(), "r") as f:
    for line in f.readlines(): 
        if line == '\n': 
            continue 
        if ',' not in line: 
            continue 

        line = line.strip().split(', ')
        if len(line) > 1: 
            towels_list += line

towels_dict = {x:True for x in towels_list}
MAX_TOWEL_LEN = max([len(x) for x in towels_dict.keys()])


@cache 
def recursively_find_all_towel_num(target_towel: str) -> int: 
    sol = recursively_find_towels(target_towel)
    if ''.join(sol) != target_towel: 
        return 0
    if len(target_towel) == 0: 
        return 0
    len_target = len(target_towel)
    successful_attempts = 0
    for i in range(1, min(len_target, 8)+1): 
        sub_string = target_towel[0:i]
        if sub_string in towels_dict.keys(): 
            if i == len_target: 
                successful_attempts += 1
            else: 
                successful_attempts += recursively_find_all_towel_num(target_towel[i:])
                    
    return successful_attempts 


@cache 
def recursively_find_towels(target_towel: str) -> dict(): 
    '''
    Try to have a memory by returning a dictionary instead 
    '''
    len_target = len(target_towel)
    #Max string length is 8
    for i in range(1, min(len_target, 8)+1): 
        sub_string = target_towel[0:i]
        if sub_string in towels_dict.keys(): 
            if i == len_target: 
                return [sub_string]
            else: 
                attempt = [sub_string] + recursively_find_towels(target_towel[i:])
                attempt_str = ''.join(attempt)
                if attempt_str == target_towel: 
                    return attempt
                else: 
                    continue 
    return []


@cache 
def recursively_find_all_towels_2(target_towel: str) -> list(): 
    sol = recursively_find_towels(target_towel)
    if ''.join(sol) != target_towel: 
        return [[]]

    #Splitting gets annoying when this isn't true 
    len_target = len(target_towel)
    if len_target < 2*MAX_TOWEL_LEN: 
        return recursively_find_all_towels(target_towel)

    #list of lists, which each one containing a possible sum 
    possible_combinations = list()
    len_target = len(target_towel)
    keys = towels_dict.keys()

    #the return all functions above is too slow as the strings are too long
    #so I am going to try splitting the strings in half
    mid_point = len_target // 2
    for i in range(mid_point, len_target+1): 
        first_half = target_towel[0:i]
        second_half = target_towel[i:len_target+1]
        
        first_half_attempt = recursively_find_towels(first_half)
        second_half_attempt = recursively_find_towels(second_half)
        
        first_half_attempt_str = ''.join(first_half_attempt)
        second_half_attempt_str = ''.join(second_half_attempt)

        if (first_half_attempt_str == first_half) and (second_half_attempt_str == second_half): 
            break 

    all_first_half_attempts = recursively_find_all_towels(first_half)
    all_second_half_attempts = recursively_find_all_towels(second_half)
    
    succ_first_half_attempts = list()
    succ_second_half_attempts = list()
    for first_half_attempt in all_first_half_attempts: 
        first_half_attempt_str = ''.join(first_half_attempt)
        if first_half_attempt_str == first_half: 
            succ_first_half_attempts.append(first_half_attempt)
    
    for second_half_attempt in all_second_half_attempts: 
        second_half_attempt_str = ''.join(second_half_attempt)
        if second_half_attempt_str == second_half: 
            succ_second_half_attempts.append(second_half_attempt)
    
    for first_half_attempt in succ_first_half_attempts: 
        for second_half_attempt in succ_second_half_attempts: 
            attempt = first_half_attempt + second_half_attempt
            possible_combinations.append(attempt)
    
    #Now need to account for things happening in the middle 
    for k in range(2, MAX_TOWEL_LEN+1): 
        print('hello')

    return [[]]


def q1(target_towels: list) -> int:
    success = 0
    for i, target_towel in enumerate(target_towels): 
        part_towel = recursively_find_towels(target_towel)
        attempt = ''.join(part_towel)

        if attempt == target_towel: 
            success += 1
        
    return success


def q2(target_towels: list) -> int: 
    success = 0
    for i, target_towel in enumerate(target_towels):
        success += recursively_find_all_towel_num(target_towel)
    
    return success


if __name__ == "__main__":
    filename = get_input_filename(__file__, is_test=False)
    _, target_towels = load_data(filename)
    print(q1(target_towels))
    print(q2(target_towels))

