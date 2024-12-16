def caclulate_area(region: list[tuple[int, int]]) -> int:
    return len(region)

def calculate_perimeter(region: list[tuple[int, int]]) -> int:
    perimeter = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for x, y in region:
        for dx, dy in directions:
            neighbor = (x + dx, y + dy)
            if neighbor not in region:
                perimeter += 1

    return perimeter

def explore_region(start_x, start_y, current_region_value, grid, visited):
    queue = [(start_x, start_y)]
    region = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        x, y = queue.pop(0)
        if (x, y) in region or (x, y) in visited:
            continue
        visited.append((x, y))
        region.append((x, y))

        for dx, dy in directions:
            if x+dx >= 0 and x+dx < len(grid) and y+dy >= 0 and y+dy < len(grid[x+dx]) and grid[x + dx][y + dy] == current_region_value:
                queue.append((x + dx, y + dy))
    return region


def main(input_string: str) -> int:
    result = 0
    rows = input_string.split('\n')
    grid = []
    regions = []

    for index, row in enumerate(rows):
        elements = list(row)
        grid.append(elements)

    visited = []
    for column_index in range(len(grid)):
        for row_index in range(len(grid[column_index])):
            region = explore_region(column_index, row_index, grid[column_index][row_index], grid, visited)
            if region:
                regions.append(region)
    
    for region in regions:
        area = caclulate_area(region)
        perimeter = calculate_perimeter(region)
        result += area * perimeter

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)