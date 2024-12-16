def try_next_position(starting_value, starting_position, grid, end_values):
    print(f"Starting value: {starting_value}, starting position: {starting_position}")
    if (starting_value == 9):
        end_values.append(starting_position)
    else:
        if (starting_position[0]+1 < len(grid) and grid[starting_position[0]+1][starting_position[1]] == starting_value + 1):
            try_next_position(starting_value + 1, (starting_position[0]+1, starting_position[1]), grid, end_values)
        if (starting_position[0]-1 >= 0 and grid[starting_position[0]-1][starting_position[1]] == starting_value + 1):
            try_next_position(starting_value + 1, (starting_position[0]-1, starting_position[1]), grid, end_values)
        if (starting_position[1]-1 >= 0 and grid[starting_position[0]][starting_position[1]-1] == starting_value + 1):
            try_next_position(starting_value + 1, (starting_position[0], starting_position[1]-1), grid, end_values)
        if (starting_position[1]+1 < len(grid[0]) and grid[starting_position[0]][starting_position[1]+1] == starting_value + 1):
            try_next_position(starting_value + 1, (starting_position[0], starting_position[1]+1), grid, end_values)
    return end_values

def main(input_string: str) -> int:
    result = 0
    lines = input_string.split("\n")
    grid = []

    paths = []
    for index, line in enumerate(lines):
        row = list(line)
        int_row = []
        for index_item, item in enumerate(row):
            int_row.append(int(item))
            if item == '0':
                paths.append((index, index_item))
        grid.append(int_row)

    for index, starting_position in enumerate(paths):
        valid_end_positions = try_next_position(0, starting_position, grid, [])
        result += len(valid_end_positions)

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)