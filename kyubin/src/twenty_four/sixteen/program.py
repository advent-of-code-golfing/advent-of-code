from collections import deque, defaultdict
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum

from src.common import Vector
from src.utils import get_input_filename


class Dir(StrEnum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


DIR_TO_VECTOR = {
    Dir.NORTH: Vector(-1, 0),
    Dir.EAST: Vector(0, 1),
    Dir.SOUTH: Vector(1, 0),
    Dir.WEST: Vector(0, -1),
}

RIGHT_MOVES = {
    Dir.NORTH: Dir.EAST,
    Dir.EAST: Dir.SOUTH,
    Dir.SOUTH: Dir.WEST,
    Dir.WEST: Dir.NORTH,
}

LEFT_MOVES = {
    Dir.NORTH: Dir.WEST,
    Dir.WEST: Dir.SOUTH,
    Dir.SOUTH: Dir.EAST,
    Dir.EAST: Dir.NORTH,
}


class Score:
    def __init__(self) -> None:
        self.score: dict[Dir, int | float] = {
            Dir.NORTH: float("inf"),
            Dir.EAST: float("inf"),
            Dir.SOUTH: float("inf"),
            Dir.WEST: float("inf"),
        }
        self.prev_pos: dict[Dir, list[Position]] = defaultdict(list)

    def __str__(self) -> str:
        north = self.score[Dir.NORTH]
        east = self.score[Dir.EAST]
        south = self.score[Dir.SOUTH]
        west = self.score[Dir.WEST]
        return f"N: {north}, E: {east}, S: {south}, W: {west}"


@dataclass
class Position:
    pos: Vector
    dir: Dir
    score: int
    prev_pos: "Position | None" = None

    def __repr__(self) -> str:
        return f"{self.pos}, {self.dir}, {self.score}"

    def get_next_positions(self) -> list["Position"]:
        dir_vector = DIR_TO_VECTOR[self.dir]
        take_step_move = Position(self.pos + dir_vector, self.dir, self.score + 1, self)
        turn_right_move = Position(self.pos, RIGHT_MOVES[self.dir], self.score + 1000, self)
        turn_left_move = Position(self.pos, LEFT_MOVES[self.dir], self.score + 1000, self)

        return [take_step_move, turn_right_move, turn_left_move]


@dataclass
class Maze:
    maze: list[list[str]]
    start: Vector
    end: Vector
    dir: Dir = Dir.EAST

    def print_maze(self, move: Position) -> None:
        self.maze[move.pos.row][move.pos.col] = move.dir.value

        for row in self.maze:
            print("".join(row))

    def can_move_to_pos(self, pos: Position) -> bool:
        return self.maze[pos.pos.row][pos.pos.col] != "#"


class ScoreBoard:
    def __init__(self, nrows: int, ncols: int) -> None:
        self.scores = [[Score() for _ in range(ncols)] for _ in range(nrows)]

    def get_score(self, pos: Position) -> int | float:
        return self.scores[pos.pos.row][pos.pos.col].score[pos.dir]

    def set_score(self, pos: Position) -> None:
        self.scores[pos.pos.row][pos.pos.col].score[pos.dir] = pos.score

    def reset_prev_pos(self, pos: Position) -> None:
        score = self.scores[pos.pos.row][pos.pos.col]
        if pos.prev_pos is None:
            return
        score.prev_pos[pos.dir] = [pos.prev_pos]

    def append_prev_pos(self, pos: Position) -> None:
        score = self.scores[pos.pos.row][pos.pos.col]
        if pos.prev_pos is None:
            return
        if pos.prev_pos not in score.prev_pos[pos.dir]:
            score.prev_pos[pos.dir].append(pos.prev_pos)

    def get_score_object_at_vec(self, vec: Vector) -> Score:
        return self.scores[vec.row][vec.col]

    def get_min_score_at_pos(self, vec: Vector) -> int | float:
        return min(self.scores[vec.row][vec.col].score.values())


def load_data(filename: str) -> Maze:
    maze: list[list[str]] = []
    with open(filename, "r") as f:
        for line in f.readlines():
            maze.append([*line.strip()])

    # Find start and end

    start, end = None, None

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "E":
                end = Vector(r, c)
            elif maze[r][c] == "S":
                start = Vector(r, c)

    if start is None or end is None:
        raise ValueError

    res = Maze(maze, start, end)

    return res


def solve_part_one(maze: Maze) -> int | float:
    # Keeps track of minimum scores at each location, facing each direction
    nrows, ncols = len(maze.maze), len(maze.maze[0])
    scoreboard = ScoreBoard(nrows, ncols)
    queue: deque[Position] = deque()
    start_pos = Position(maze.start, Dir.EAST, 0)
    queue.append(start_pos)

    while queue:
        # DFS
        cur = queue.popleft()
        next_steps = cur.get_next_positions()
        for pos in next_steps:
            if maze.can_move_to_pos(pos) and scoreboard.get_score(pos) > pos.score:
                scoreboard.set_score(pos)
                queue.append(pos)
    
    return scoreboard.get_min_score_at_pos(maze.end)


def solve_part_two(maze: Maze) -> int | float:
    # Keeps track of minimum scores at each location, facing each direction
    nrows, ncols = len(maze.maze), len(maze.maze[0])
    scoreboard = ScoreBoard(nrows, ncols)
    queue: deque[Position] = deque()
    start_pos = Position(maze.start, Dir.EAST, 0)
    queue.append(start_pos)

    while queue:
        # DFS
        cur = queue.popleft()
        next_steps = cur.get_next_positions()
        for pos in next_steps:
            if maze.can_move_to_pos(pos) is False:
                continue
            if scoreboard.get_score(pos) > pos.score:
                scoreboard.set_score(pos)
                scoreboard.reset_prev_pos(pos)
                queue.append(pos)
            if scoreboard.get_score(pos) == pos.score:
                scoreboard.append_prev_pos(pos)

    # Starting from end pos, backtrack to start
    in_best_path: set[Vector] = set()


    end_score = scoreboard.get_score_object_at_vec(maze.end)
    in_best_path.add(maze.end)
    queue: deque[Position] = deque()
    min_dir = min(end_score.score.keys(), key=lambda x: end_score.score[x])
    positions = end_score.prev_pos[min_dir]
    queue.extend(positions)

    while queue:
        cur = queue.popleft()
        # Don't loop around starting point
        in_best_path.add(cur.pos)
        if cur.pos == maze.start:
            continue
        score = scoreboard.get_score_object_at_vec(cur.pos)
        previous_positions = score.prev_pos[cur.dir]
        # print(queue)

        queue.extend(previous_positions)

    # print(in_best_path)
    
    return len(in_best_path)

def run_program(test: bool) -> None:
    filename = get_input_filename(__file__, test)
    data = load_data(filename)

    if test:
        print(solve_part_one(deepcopy(data)))
        print(solve_part_two(deepcopy(data)))
    else:
        print(solve_part_one(data))
        print(solve_part_two(data))


if __name__ == "__main__":
    run_program(False)
