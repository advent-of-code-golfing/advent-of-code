def get_new_numbers(numbers):
    new_numbers = []
    for number in numbers:
        if number == '0':
            new_numbers.append('1')
            continue
        split_numbers = list(number)
        if len(split_numbers) % 2 == 0:
            midway = len(split_numbers) // 2
            first_part = split_numbers[:midway]
            new_first_part = ''.join(first_part)
            new_numbers.append(str(int(new_first_part)))

            second_part = split_numbers[midway:]
            new_second_part = ''.join(second_part)
            new_numbers.append(str(int(new_second_part)))
        else:
            new_numbers.append(str(int(number) * 2024))
    return new_numbers

def main(input_string: str) -> int:
    numbers = input_string.split(" ")

    for i in range(25):
        numbers = get_new_numbers(numbers) 

    result = len(numbers)
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)