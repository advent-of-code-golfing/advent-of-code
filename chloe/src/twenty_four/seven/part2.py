def can_reach_expected_value(values: list[int], expected_value: int, current_value: int = 0, index: int = 0) -> bool:
    if index == len(values):
        return current_value == expected_value
    if can_reach_expected_value(values, expected_value, current_value + values[index], index + 1):
        return True
    if can_reach_expected_value(values, expected_value, current_value * values[index], index + 1):
        return True
    
    concatenated_value = int(str(current_value) + str(values[index]))
    if can_reach_expected_value(values, expected_value, concatenated_value, index + 1):
        return True

    return False


def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    for line in lines:
        expected_value = int(line.split(": ")[0])
        values = list(map(int, line.split(": ")[1].split(" ")))

        if can_reach_expected_value(values, expected_value):
            result += expected_value
        

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)