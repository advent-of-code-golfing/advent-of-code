def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    grid = [list(line) for line in lines]

    for i in range(1, len(grid)-1):
        for j in range(1, len(grid[i])-1):
            if grid[i][j] == "A":
                number_of_mas = 0
                if grid[i-1][j-1] == "M" and grid[i+1][j+1] == "S":
                    number_of_mas += 1
                if grid[i+1][j+1] == "M" and grid[i-1][j-1] == "S":
                    number_of_mas += 1
                if grid[i-1][j+1] == "M" and grid[i+1][j-1] == "S":
                    number_of_mas += 1
                if grid[i+1][j-1] == "M" and grid[i-1][j+1] == "S":
                    number_of_mas += 1
                if number_of_mas == 2:
                    result += 1
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)

