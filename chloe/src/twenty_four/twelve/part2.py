def caclulate_area(region: list[tuple[int, int]]) -> int:
    return len(region)


def calculate_unique_edges(region: list[tuple[int, int]]) -> int:
    edges = 0
    right_angles = []
    # The number of edges is equivalent to the number of right angles
    # We will say that the characteristics of a right angle is:
    # A point with the x,y coordinates of the two points which are
    # not in the region (i.e. that make it a right angle)

    #  1 2 3
    #  4 P 5
    #  6 7 8

    for x, y in region:
        top_left = (x-1, y-1) # 1
        top_middle = (x, y-1) # 2
        top_right = (x+1, y-1) # 3
        left_middle = (x-1, y) # 4
        right_middle = (x+1, y) # 5
        bottom_left = (x-1, y+1) # 6
        bottom_middle = (x, y+1) # 7
        bottom_right = (x+1, y+1) # 8

        if (top_middle not in region and left_middle not in region) or (
            top_middle in region and left_middle in region and top_left not in region):
            right_angles.append(((x,y), top_middle, left_middle))
            
        if (top_middle not in region and right_middle not in region) or (
            top_middle in region and right_middle in region and top_right not in region):
            right_angles.append(((x,y), top_middle, right_middle))

        if (bottom_middle not in region and right_middle not in region) or (
            bottom_middle in region and right_middle in region and bottom_right not in region):
            right_angles.append(((x,y), bottom_middle, right_middle))

        if (bottom_middle not in region and left_middle not in region) or (
            bottom_middle in region and left_middle in region and bottom_left not in region):
            right_angles.append(((x,y), bottom_middle, left_middle))

    return len(set(right_angles))

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
        edges = calculate_unique_edges(region)
        result += area * edges

    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)