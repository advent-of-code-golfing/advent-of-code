import re
from collections import Counter
import matplotlib.pyplot as plt

def main(input_string: str) -> int:
    width = 101
    height = 103

    pattern = r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)"
    matches = re.findall(pattern, input_string)

    for no_seconds_passed in range(10000):
        end_positions = []
        for match in matches:
            p_x, p_y, v_x, v_y = map(int, match)

            raw_end_x = p_x + v_x * no_seconds_passed
            raw_end_y = p_y + v_y * no_seconds_passed

            end_x = raw_end_x % width
            end_y = raw_end_y % height

            end_positions.append((end_x, end_y))

        x_array = [position[0] for position in end_positions]
        x_array_counter = Counter(x_array)
        y_array = [position[1] for position in end_positions]
        y_array_counter = Counter(y_array)

        if any(count > 33 for count in x_array_counter.values()) or any(count > 33 for count in y_array_counter.values()):
            plt.figure(figsize=(10, 10))
            plt.scatter(x_array, y_array, c='black', marker='s')
            plt.xlim(0, width)
            plt.ylim(0, height)
            plt.gca().invert_yaxis() 
            plt.title(f"Positions at {no_seconds_passed} seconds")
            plt.xlabel("X Position")
            plt.ylabel("Y Position")
            plt.grid(True)
            plt.show()
        

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)