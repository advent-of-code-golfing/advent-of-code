import re

def main(input_string: str) -> int:
    result = 0
    width = 101
    height = 103
    no_seconds_passed = 100

    end_positions = []
    pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    matches = re.findall(pattern, input_string)

    for match in matches:
        p_x, p_y, v_x, v_y = map(int, match)

        raw_end_x = p_x + v_x * no_seconds_passed
        raw_end_y = p_y + v_y * no_seconds_passed

        end_x = raw_end_x % width
        end_y = raw_end_y % height

        end_positions.append((end_x, end_y))

    quadrant_top_left = []
    quadrant_top_right = []
    quadrant_bottom_left = []
    quadrant_bottom_right = []


    x_center_lower = width // 2 - 1   
    x_center_upper = width // 2 + 1

    y_center_lower = height // 2 - 1
    y_center_upper = height // 2 + 1
    
    for position in end_positions:
        if position[0] <= x_center_lower and position[1] <= y_center_lower:
            quadrant_top_left.append(position)
        elif position[0] <= x_center_lower and position[1] >= y_center_upper:
            quadrant_bottom_left.append(position)
        elif position[0] >= x_center_upper and position[1] <= y_center_lower:
            quadrant_top_right.append(position)
        elif position[0] >= x_center_upper and position[1] >= y_center_upper:
            quadrant_bottom_right.append(position)

    result = len(quadrant_top_left) * len(quadrant_top_right) * len(quadrant_bottom_left) * len(quadrant_bottom_right)
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)