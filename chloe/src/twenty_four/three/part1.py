import re
def main(input_string: str) -> int:
    lines = input_string.split("\n")

    pattern = r'mul\((\d+),(\d+)\)'
    result = 0

    for line in lines:
        matches = re.findall(pattern, line)

        for match in matches:
            x, y = match
            result += int(x) * int(y)

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)