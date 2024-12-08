def main(input_string: str) -> int:
    lines = input_string.split("\n")
    antenas = {}
    antinodes = []

    for i in range(len(lines)):
        characters = list(lines[i])
        for j in range(len(characters)):
            if characters[j] != ".":
                antinodes.append((i, j))
                if (characters[j] not in antenas):
                    antenas[characters[j]] = [(i, j)]
                else:
                    antenas[characters[j]].append((i, j))
    
    for antenna in antenas:
        for i in range(len(antenas[antenna])):
            for j in range(i + 1, len(antenas[antenna])):
                x1 = antenas[antenna][i][0]
                x2 = antenas[antenna][j][0]
                y1 = antenas[antenna][i][1]
                y2 = antenas[antenna][j][1]
                x_diff = x1 - x2
                y_diff = y1 - y2

                while x1+x_diff >= 0 and x1+x_diff < len(lines) and y1+y_diff >= 0 and y1+y_diff < len(lines[0]):
                    antinodes.append((x1+x_diff, y1+y_diff))
                    x1 += x_diff    
                    y1 += y_diff
                while x2-x_diff >= 0 and x2-x_diff < len(lines) and y2-y_diff >= 0 and y2-y_diff < len(lines[0]):
                    antinodes.append((x2-x_diff, y2-y_diff))
                    x2 -= x_diff
                    y2 -= y_diff
    antinodes = list(set(antinodes))
    result = len(antinodes)
    
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)