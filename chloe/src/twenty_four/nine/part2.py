from collections import OrderedDict

def main(input_string: str) -> int:
    result = 0
    final_string_values = []
    files_with_numbers = {}
    blank_spaces = OrderedDict()
    non_blank_spaces = OrderedDict()
    index_files = 0
    global_index = 0

    values = [int(char) for char in input_string]

    for i in range(len(values)):
        if i % 2 == 0:
            non_blank_spaces[index_files] = global_index
            for j in range(values[i]):
                final_string_values.append(index_files)
                global_index += 1
            files_with_numbers[index_files] = values[i]
            index_files += 1
        else: 
            blank_spaces[global_index] = values[i]
            for j in range(values[i]):
                final_string_values.append('.')
                global_index += 1

    for key in sorted(files_with_numbers.keys(), reverse=True):
        starting_index_non_blank_spaces = non_blank_spaces[key]
        for starting_index, number_of_blank_spaces in blank_spaces.items():
            if number_of_blank_spaces >= files_with_numbers[key] and starting_index < starting_index_non_blank_spaces:
                for i in range(files_with_numbers[key]):
                    final_string_values[starting_index + i] = key

                for i in range(files_with_numbers[key]):
                    final_string_values[starting_index_non_blank_spaces + i] = '.'
                del blank_spaces[starting_index]
                if number_of_blank_spaces - files_with_numbers[key] > 0:
                    blank_spaces[starting_index + files_with_numbers[key]] = number_of_blank_spaces - files_with_numbers[key]
                    blank_spaces = OrderedDict(sorted(blank_spaces.items()))
                break

    for i in range(len(final_string_values)):
        if i < 50:
            print(f"File {final_string_values[i]} at index {i}")
        if final_string_values[i] != '.':
            result += final_string_values[i] * (i)
    
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)
