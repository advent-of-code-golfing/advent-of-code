def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")

    rules = []
    lines_to_check = []
    for line in lines:
        if line == "":
            continue
        if "|" in line:
            values = line.split("|")
            rules.append((int(values[0]), int(values[1])))
        else:
            is_valid = True
            values = [int(value) for value in line.split(",")]

            while True:
                made_swap = False
                for rule in rules:
                    first, second = rule
                    if first in values and second in values:
                        index_first = values.index(first)
                        index_second = values.index(second)
                        if index_first > index_second:
                            is_valid = False
                            values[index_first], values[index_second] = values[index_second], values[index_first]
                            made_swap = True
                if not made_swap:
                    break
     
            if not is_valid:
                result += int(values[(len(values) - 1) // 2])
                
    
    print(result)

    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)