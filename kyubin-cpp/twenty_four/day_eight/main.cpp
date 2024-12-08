#include <iostream>
#include <fstream>
#include <map>

struct Vec {
    int row;
    int col;
};

struct InputData {
    std::vector<std::string> map{};
    std::vector<std::string> antinode{};
    std::map<char, std::vector<Vec> > locations{};
};

bool within_range(const int& nrows, const int& ncols, const int& row, const int& col) {
    return row >= 0 && row < nrows && col >= 0 && col < ncols;
}

InputData load_data(const std::string &filename) {
    std::ifstream file(filename);

    InputData data;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return data;
    }

    std::string line;

    int row = 0;

    while (std::getline(file, line)) {
        data.map.push_back(line);
        for (int col = 0; col < line.size(); col++) {
            if (line[col] == '.') {
                continue;
            }
            if (!data.locations.contains(line[col])) {
                data.locations[line[col]] = std::vector<Vec>{};
            }
            data.locations[line[col]].push_back(Vec{row, col});
        }
        data.antinode.push_back(std::string(line.size(), '.'));
        row++;
    }
    return data;
}

void print_antinodes(std::vector<std::string>& antinode) {
    for (const auto &row : antinode) {
        std::cout << row << std::endl;
    }
    std::cout << std::endl;
}

int solve_part_one(InputData data) {
    int nrows = data.map.size();
    int ncols = data.map[0].size();

    for (auto antenna : data.locations) {
        int n = antenna.second.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (i == j){continue;}
                Vec a1 = antenna.second[i];
                Vec a2 = antenna.second[j];
                int new_row;
                int new_col;
                Vec a1_a2 = Vec{a2.row - a1.row, a2.col - a1.col};
                new_row = a1.row - a1_a2.row;
                new_col = a1.col - a1_a2.col;
                // std::cout << antenna.first << " " << new_row << " " << new_col << std::endl;
                if (within_range(nrows, ncols, new_row, new_col)) {
                    data.antinode[new_row][new_col] = '#';
                    // print_antinodes(data.antinode);
                }
                new_row = a2.row + a1_a2.row;
                new_col = a2.col + a1_a2.col;
                // std::cout << antenna.first << " " << new_row << " " << new_col << std::endl;
                if (within_range(nrows, ncols, new_row, new_col)) {
                    data.antinode[new_row][new_col] = '#';
                    // print_antinodes(data.antinode);
                }
            }
        }
    }
    int tot = 0;
    for (auto row : data.antinode) {
        for (auto val : row) {
            if (val == '#') {
                tot++;
            }
        }
    }
    return tot;
}

Vec reduce(Vec vector) {
    int min_val = std::min(vector.row, vector.col);
    if (vector.row % min_val == 0 and vector.col % min_val == 0) {
        return Vec{vector.row / min_val, vector.col / min_val};
    }
    return vector;
}

int solve_part_two(InputData data) {
    int nrows = data.map.size();
    int ncols = data.map[0].size();

    for (auto antenna : data.locations) {
        int n = antenna.second.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                if (i == j){continue;}
                Vec a1 = antenna.second[i];
                Vec a2 = antenna.second[j];
                int new_row;
                int new_col;
                Vec a1_a2_old = Vec{a2.row - a1.row, a2.col - a1.col};
                Vec a1_a2 = reduce(a1_a2_old);

                new_row = a1.row;
                new_col = a1.col;
                // std::cout << antenna.first << " " << new_row << " " << new_col << std::endl;
                while (within_range(nrows, ncols, new_row, new_col)) {
                    data.antinode[new_row][new_col] = '#';
                    new_row -= a1_a2.row;
                    new_col -= a1_a2.col;
                }
                new_row = a1.row + a1_a2.row;
                new_col = a1.col + a1_a2.col;
                // std::cout << antenna.first << " " << new_row << " " << new_col << std::endl;
                while (within_range(nrows, ncols, new_row, new_col)) {
                    data.antinode[new_row][new_col] = '#';
                    new_row += a1_a2.row;
                    new_col += a1_a2.col;
                    // print_antinodes(data.antinode);
                }
            }
        }
    }
    print_antinodes(data.antinode);
    int tot = 0;
    for (auto row : data.antinode) {
        for (auto val : row) {
            if (val == '#') {
                tot++;
            }
        }
    }
    return tot;
}

int main() {
    const bool test = false;
    std::string filename;
    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }
    InputData data = load_data(filename);
    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;

    return 0;
}
