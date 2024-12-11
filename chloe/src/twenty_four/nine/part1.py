def main(input_string: str) -> int:
    result = 0
    final_string_values = []
    indices_with_values = []
    index_files = 0
    global_index = 0

    values = [int(char) for char in input_string]

    for i in range(len(values)):
        if i % 2 == 0:
            for j in range(values[i]):
                final_string_values.append(index_files)
                indices_with_values.append(global_index)
                global_index += 1
            index_files += 1
        else: 
            for j in range(values[i]):
                final_string_values.append('.')
                global_index += 1

    for index, value in enumerate(final_string_values):
        if index > indices_with_values[-1]:
            break
        elif value == '.':
            indices_of_value_to_replace = indices_with_values.pop(-1)
            final_string_values[index] = final_string_values[indices_of_value_to_replace]
            final_string_values[indices_of_value_to_replace] = '.'
        result += index * final_string_values[index]

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)