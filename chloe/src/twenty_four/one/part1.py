from utils import read_file_to_string, split_input
def order_columns(column1: list[int], column2: list[int]) -> tuple[list[int], list[int]]:
    return sorted(column1), sorted(column2)

def calculate_difference(column1: list[int], column2: list[int]) -> int:
    return sum(abs(value1 - value2) for value1, value2 in zip(column1, column2))

def main(input_string: str) -> int:
    column1, column2 = split_input(input_string)
    column1_sorted, column2_sorted = order_columns(column1, column2)
    calculate_difference(column1_sorted, column2_sorted)

if __name__ == "__main__":
    file_path = 'input.txt'
    file_contents = read_file_to_string(file_path)
    main(file_contents)
