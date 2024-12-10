#include <iostream>
#include <fstream>
#include <queue>

struct Vec {
    int row;
    int col;

    bool operator==(const Vec& rhs) const {
        return row == rhs.row && col == rhs.col;
    }

    Vec operator+(const Vec& rhs) const {
        return Vec{row + rhs.row, col + rhs.col};
    }
};

class TrailMap {
public:
    std::vector<std::vector<int>> map;
    std::vector<Vec> starting_points;
    int nrows;
    int ncols;

    TrailMap(std::vector<std::vector<int>> map_input, std::vector<Vec> starting_point_input) {
        map = map_input;
        starting_points = starting_point_input;
        nrows = map.size();
        ncols = map[0].size();
    }

    TrailMap();


    [[nodiscard]] bool within_range(const Vec& vec) const {
        return vec.row >= 0 && vec.row < nrows && vec.col >= 0 && vec.col < ncols;
    }

    [[nodiscard]] int get_val(const Vec& vec) const {
        return map[vec.row][vec.col];
    }


};

TrailMap load_data(std::string &filename) {
    std::ifstream file(filename);
    // if (!file.is_open()) {
    //     std::cerr << "Error opening file" << std::endl;
    //     return TrailMap{};
    // }

    std::string line;

    std::vector<std::vector<int>> lines;
    std::vector<Vec> starting_points;

    int row = 0;


    while (std::getline(file, line)) {
        std::vector<int> cur_row;
        for (int col = 0; col < line.size(); col++) {
            cur_row.push_back(line[col] - '0');
            if (line[col] == '0') {
                starting_points.push_back(Vec{row, col});
            }
        }
        lines.push_back(cur_row);
        row++;
    }

    TrailMap map(lines, starting_points);
    return map;
}

int bfs(const TrailMap& map, Vec start, int part) {
    const std::vector<Vec> dirs = {
        Vec{1, 0},
        Vec{-1, 0},
        Vec{0, 1},
        Vec{0, -1}
    };
    // FIFO queue
    std::queue<Vec> q;
    q.push(start);
    std::vector<Vec> ends;
    int paths = 0;

    while (!q.empty()) {
        Vec curr = q.front();
        int cur_val = map.get_val(curr);
        if (cur_val == 9) {
            paths++;
            if (!(std::ranges::find(ends, curr) != ends.end())) {
                ends.push_back(curr);
            }
        }
        q.pop();
        for (auto dir : dirs) {
            Vec next = curr + dir;
            if (!map.within_range(next)){
                continue;
            }
            int val = map.get_val(next);
            if (val == cur_val + 1) {
                q.push(next);
                // std::cout << "Adding " << next.row << " " << next.col << std::endl;
            }
        }
    }
    // std::cout << "Ends: ";
    // for (auto end : ends) {
    //     std::cout << end.row << "," << end.col << " ";
    // }
    // std::cout << std::endl;
    if (part == 1) {
        return ends.size();
    } else {
        return paths;
    }

}

int solve_part_one(TrailMap map) {
    // DFS to find trail starting from each starting point
    int total = 0;
    for (auto start : map.starting_points) {
        int res = bfs(map,start,1);
        // std::cout << start.row << " " << start.col << " " << res << std::endl;
        total += res;
    }
    return total;
}

int solve_part_two(TrailMap map) {
    // DFS to find trail starting from each starting point
    int total = 0;
    for (auto start : map.starting_points) {
        int res = bfs(map,start,2);
        // std::cout << start.row << " " << start.col << " " << res << std::endl;
        total += res;
    }
    return total;
}


int main() {
    const bool test = false;
    std::string filename;
    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }
    TrailMap map = load_data(filename);
    std::cout << solve_part_one(map) << std::endl;
    std::cout << solve_part_two(map) << std::endl;

    return 0;
}
