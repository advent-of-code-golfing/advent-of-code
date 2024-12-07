from utils import rotate_direction
def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    grid = []
    direction = (0, -1)
    current_x = 0
    current_y = 0

    for i, line in enumerate(lines):
        row = list(line)
        grid.append(row)
        for j, char in enumerate(row):
            if char == "^":
                current_x = j
                current_y = i

    is_in_grid = True
    while is_in_grid:
        if grid[current_y][current_x] != "X":
            result += 1
            grid[current_y][current_x] = "X"
        direction_x, direction_y = direction

        if (current_y + direction_y < 0 or current_y + direction_y >= len(grid) or
            current_x + direction_x < 0 or current_x + direction_x >= len(grid[0])):
            is_in_grid = False
            break

        if grid[current_y + direction_y][current_x + direction_x] == "#":
            direction = rotate_direction(direction)
        else: 
            current_x += direction_x
            current_y += direction_y

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)