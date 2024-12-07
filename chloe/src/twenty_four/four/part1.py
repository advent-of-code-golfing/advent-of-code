def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    grid = [list(line) for line in lines]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                if i+3 < len(grid) and grid[i+1][j] == "M" and grid[i+2][j] == "A" and grid[i+3][j] == "S":
                    result += 1
                if i-3 >= 0 and grid[i-1][j] == "M" and grid[i-2][j] == "A" and grid[i-3][j] == "S":
                    result += 1
                if j+3 < len(grid[i]) and grid[i][j+1] == "M" and grid[i][j+2] == "A" and grid[i][j+3] == "S":
                    result += 1
                if j-3 >= 0 and grid[i][j-1] == "M" and grid[i][j-2] == "A" and grid[i][j-3] == "S":
                    result += 1
                if i+3 < len(grid) and j+3 < len(grid[i]) and grid[i+1][j+1] == "M" and grid[i+2][j+2] == "A" and grid[i+3][j+3] == "S":
                    result += 1
                if i-3 >= 0 and j-3 >= 0 and grid[i-1][j-1] == "M" and grid[i-2][j-2] == "A" and grid[i-3][j-3] == "S":
                    result += 1
                if i+3 < len(grid) and j-3 >= 0 and grid[i+1][j-1] == "M" and grid[i+2][j-2] == "A" and grid[i+3][j-3] == "S":
                    result += 1
                if i-3 >= 0 and j+3 < len(grid[i]) and grid[i-1][j+1] == "M" and grid[i-2][j+2] == "A" and grid[i-3][j+3] == "S":
                    result += 1

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)