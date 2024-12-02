def main(input_string: str) -> int:
    lines = input_string.split("\n")
    number_of_safe_reports = 0
    for line in lines:
        values = list(map(int, line.split()))
        print("------")
        print(values)

        def is_safe_sequence(values):
            is_increasing_and_valid = all(values[i] < values[i+1] and 1 <= values[i+1] - values[i] <= 3 for i in range(len(values) - 1))
            is_decreasing_and_valid = all(values[i] > values[i+1] and 1 <= values[i] - values[i+1] <= 3 for i in range(len(values) - 1))
            return is_increasing_and_valid or is_decreasing_and_valid

        if is_safe_sequence(values):
            number_of_safe_reports += 1
            continue

        for i in range(len(values)):
            if is_safe_sequence(values[:i] + values[i+1:]):
                number_of_safe_reports += 1
                break

    print("number of safe reports", number_of_safe_reports)
    return number_of_safe_reports

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)