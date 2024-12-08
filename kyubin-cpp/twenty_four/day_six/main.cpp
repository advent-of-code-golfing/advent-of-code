#include <iostream>
#include <fstream>
#include <map>
#include <set>

struct Vec {
    int row;
    int col;

    bool operator==(const Vec& rhs) const {
        return row == rhs.row && col == rhs.col;
    }

    bool operator<(const Vec& rhs) const {
        return row < rhs.row || (row == rhs.row && col < rhs.col);
    }
};

class Map {
public:
    Vec current{};
    std::vector<std::vector<char> > map{};
    char direction{};
    std::map<char, Vec> direction_map{
        {'^', Vec{-1, 0}},
        {'>', Vec{0, 1}},
        {'v', Vec{1, 0}},
        {'<', Vec{0, -1}},
    };
    Vec size{};

    Vec direction_vector() {
        return direction_map[direction];
    }

    [[nodiscard]] char direction_to_right() const {
        if (direction == '^') {
            return '>';
        }
        if (direction == '>') {
            return 'v';
        }
        if (direction == 'v') {
            return '<';
        }
        return '^';
    }

    void turn_right() {
        direction = direction_to_right();
    }

    [[nodiscard]] bool within_range(const Vec &point) const {
        return point.row >= 0 && point.row < size.row && point.col >= 0 && point.col < size.col;
    }

    [[nodiscard]] bool is_obstacle(const Vec &point) const {
        return map[point.row][point.col] == '#';
    }

    [[nodiscard]] Vec next_point() {
        return Vec{current.row + direction_vector().row, current.col + direction_vector().col};
    }

    [[nodiscard]] int count_been() const {
        int total = 0;
        for (int row = 0; row < size.row; row++) {
            for (int col = 0; col < size.col; col++) {
                if (const char cur = map[row][col]; cur == '^' || cur == '>' || cur == 'v' || cur == '<') {
                    total++;
                }
            }
        }
        return total;
    }

    void print_map() const {
        for (int row = 0; row < size.row; row++) {
            for (int col = 0; col < size.col; col++) {
                std::cout << map[row][col] << " ";
            }
            std::cout << std::endl;
        }
        std::cout << std::endl;
    }
};


Map load_data(const std::string &filename) {
    std::ifstream file(filename);
    Map map{};

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return map;
    }

    std::string line;

    int row = 0;

    while (std::getline(file, line)) {
        std::vector<char> current_row{};
        for (int col = 0; col < line.length(); col++) {
            current_row.push_back(line.at(col));
            if (line[col] == '^') {
                map.current = Vec{row, col};
                map.direction = line[col];
            } else if (line[col] == '>') {
                map.current = Vec{row, col};
                map.direction = line[col];
            } else if (line[col] == 'v') {
                map.current = Vec{row, col};
                map.direction = line[col];
            } else if (line[col] == '<') {
                map.current = Vec{row, col};
                map.direction = line[col];
            }
        }
        map.map.push_back(current_row);
        row++;
    }
    map.size = Vec{static_cast<int>(map.map.size()), static_cast<int>(map.map[0].size())};
    return map;
}

int solve_part_one(Map map) {
    while (true) {
        // std::cout << map.current.row << " " << map.current.col << std::endl;
        // map.print_map();
        Vec next = map.next_point();
        if (!map.within_range(next)) {
            return map.count_been();
        }
        if (map.is_obstacle(next)) {
            map.turn_right();
            continue;
        }
        if (map.direction == map.map[next.row][next.col]) {
            return map.count_been();
        }
        map.map[next.row][next.col] = map.direction;
        map.current = next;
    }
}

bool add_obstacle_and_check_loop(Map map, Vec obstacle) {
    map.map[obstacle.row][obstacle.col] = '#';
    while (true) {
        Vec next = map.next_point();
        if (!map.within_range(next)) {
            return false;
        }
        if (map.is_obstacle(next)) {
            map.turn_right();
            continue;
        }
        if (map.direction == map.map[next.row][next.col]) {
            // map.print_map();
            return true;
        }
        map.map[next.row][next.col] = map.direction;
        map.current = next;
    }
}

int solve_part_two(Map map) {
    // std::cout << map.current.row << " " << map.current.col << std::endl;
    // map.print_map();
    int additional_obstacles = 0;

    for (int row = 0; row < map.size.row; row++) {
        for (int col = 0; col < map.size.col; col++) {
            if (map.map[row][col] == '.') {
                if (add_obstacle_and_check_loop(map, Vec{row, col})) {
                    additional_obstacles++;
                }
            }
        }
    }
    return additional_obstacles;
}


int main() {
    const bool test = false;
    std::string filename;

    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }

    Map data = load_data(filename);
    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;
}
