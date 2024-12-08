def main(input_string: str) -> int:
    lines = input_string.split("\n")
    antenas = {}
    for i in range(len(lines)):
        characters = list(lines[i])
        for j in range(len(characters)):
            if characters[j] != ".":
                if (characters[j] not in antenas):
                    antenas[characters[j]] = [(i, j)]
                else:
                    antenas[characters[j]].append((i, j))
    
    antinodes = []
    for antenna in antenas:
        for i in range(len(antenas[antenna])):
            for j in range(i + 1, len(antenas[antenna])):
                x_diff = antenas[antenna][i][0] - antenas[antenna][j][0]
                y_diff = antenas[antenna][i][1] - antenas[antenna][j][1]
                if antenas[antenna][i][0]+x_diff >= 0 and antenas[antenna][i][0]+x_diff < len(lines) and antenas[antenna][i][1]+y_diff >= 0 and antenas[antenna][i][1]+y_diff < len(lines[0]):
                    antinodes.append((antenas[antenna][i][0]+x_diff, antenas[antenna][i][1]+y_diff))
                if antenas[antenna][j][0]-x_diff >= 0 and antenas[antenna][j][0]-x_diff < len(lines) and antenas[antenna][j][1]-y_diff >= 0 and antenas[antenna][j][1]-y_diff < len(lines[0]):
                    antinodes.append((antenas[antenna][j][0]-x_diff, antenas[antenna][j][1]-y_diff))
    antinodes = list(set(antinodes))
    result = len(antinodes)
    
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)