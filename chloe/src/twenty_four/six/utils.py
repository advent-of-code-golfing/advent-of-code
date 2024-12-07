def rotate_direction(direction: tuple[int, int]) -> tuple[int, int]:
    direction_x, direction_y = direction
    if direction_x == 0 and direction_y == -1:
        return (1, 0)
    elif direction_x == 0 and direction_y == 1:
        return (-1, 0)
    elif direction_x == 1 and direction_y == 0:
        return (0, 1)
    elif direction_x == -1 and direction_y == 0:
        return (0, -1)
