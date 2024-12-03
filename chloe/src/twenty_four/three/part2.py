import re
def main(input_string: str) -> int:
    lines = input_string.split("\n")

    pattern = r'mul\((\d+),(\d+)\)|do\(\)|don\'t\(\)'
    result = 0

    is_calculating = True

    for line in lines:
        matches = re.finditer(pattern, line)

        for match in matches:
            group = match.group(0)
            if group == "do()":
                is_calculating = True
            elif group == "don't()":
                is_calculating = False
            else:
                if is_calculating:
                    x, y = match.group(1), match.group(2)
                    result += int(x) * int(y)

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)

