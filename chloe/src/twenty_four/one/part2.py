from utils import read_file_to_string, split_input

def main(input_string: str) -> int:
    column1, column2 = split_input(input_string)
    return sum(column2.count(item) * item for item in column1)

if __name__ == "__main__":
    file_path = 'input.txt'
    file_contents = read_file_to_string(file_path)
    main(file_contents)