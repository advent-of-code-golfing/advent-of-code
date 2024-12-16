def get_new_numbers(set_numbers):
    new_set = {}
    
    for number, count in set_numbers.items():
        if number == '0':
            new_set['1'] = new_set.get('1', 0) + count
            continue
        
        split_numbers = list(number)
        if len(split_numbers) % 2 == 0:
            midway = len(split_numbers) // 2
            first_part = ''.join(split_numbers[:midway])
            second_part = ''.join(split_numbers[midway:])
            
            new_first_part = str(int(first_part))
            new_second_part = str(int(second_part))
            
            new_set[new_first_part] = new_set.get(new_first_part, 0) + count
            new_set[new_second_part] = new_set.get(new_second_part, 0) + count
        else:
            new_value = str(int(number) * 2024)
            new_set[new_value] = new_set.get(new_value, 0) + count

    return new_set

def main(input_string: str) -> int:
    numbers = input_string.split()
    set_numbers = {number: numbers.count(number) for number in set(numbers)}

    for _ in range(75):
        set_numbers = get_new_numbers(set_numbers)

    result = sum(set_numbers.values())
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)