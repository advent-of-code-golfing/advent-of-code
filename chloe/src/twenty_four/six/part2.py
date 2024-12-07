from utils import rotate_direction

def simulate_attempted_loop(grid: list[list[str]], start_x: int, start_y: int, direction: tuple[int, int]) -> bool:
    visited = set()
    current_x = start_x
    current_y = start_y
    direction_x, direction_y = direction

    while True:
        if (current_x, current_y, direction) in visited:
            return True
        visited.add((current_x, current_y, direction))

        if (current_y + direction_y < 0 or current_y + direction_y >= len(grid) or
            current_x + direction_x < 0 or current_x + direction_x >= len(grid[0])):
            return False

        if grid[current_y + direction_y][current_x + direction_x] == "#":
            direction = rotate_direction(direction)
            direction_x, direction_y = direction
        else:
            current_x += direction_x
            current_y += direction_y
        

def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    grid = []
    direction = (0, -1)
    start_x = 0
    start_y = 0

    for i, line in enumerate(lines):
        row = list(line)
        grid.append(row)
        for j, char in enumerate(row):
            if char == "^":
                start_x = j
                start_y = i


    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) == (start_x, start_y) or grid[y][x] == "#":
                continue

            grid[y][x] = "#"
            if simulate_attempted_loop(grid, start_x, start_y, direction):
                result += 1
            grid[y][x] = "."

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)