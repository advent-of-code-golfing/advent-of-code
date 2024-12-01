def read_file_to_string(file_path: str) -> str:
    with open(file_path, 'r') as file:
        data = file.read()
    return data


def split_input(input_string: str) -> tuple[list[int], list[int]]:
    lines = input_string.split("\n")
    column1, column2 = zip(*(map(int, line.split()) for line in lines))

    return list(column1), list(column2)