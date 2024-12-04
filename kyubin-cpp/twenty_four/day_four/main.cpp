#include <iostream>
#include <fstream>
#include <string>

std::vector<std::string> load_data(const std::string &filename) {
    std::ifstream file(filename);

    std::vector<std::string> res = {};

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return res;
    }

    std::string line;


    while (std::getline(file, line)) {
        res.push_back(line);
    }
    return res;
}

bool within_range(const int rows, const int cols, const int row, const int col) {
    return row >= 0 && row <= rows && col >= 0 && col <= cols;
}


int solve_part_one(const std::vector<std::string> &input) {
    const int num_rows = input.size();
    const int num_cols = input[0].size();

    const std::vector<int> dirs = {0, 1, -1};
    const std::vector<char> letters = {'M', 'A', 'S'};

    int xmas_count = 0;

    for (int row = 0; row < num_rows; row++) {
        for (int col = 0; col < num_cols; col++) {
            if (input[row][col] != 'X') {
                continue;
            }
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    if (!within_range(num_rows, num_cols, row + 3 * dr, col + 3 * dc)) {
                        continue;
                    }
                    bool found = true;
                    for (int i = 0; i < letters.size(); i++) {
                        char cur = input[row + (i + 1) * dr][col + (i + 1) * dc];
                        if (cur != letters[i]) {
                           found = false;
                        }
                    }
                    if (found) {
                        std::cout << "Found XMAS: " << row << " " << col;
                        std::cout << " DIR: " << dr << " " << dc << std::endl;
                        xmas_count++;
                    }

                }
            }
        }
    }
    return xmas_count;
}

int solve_part_two(const std::vector<std::string> &input) {
    const int num_rows = input.size();
    const int num_cols = input[0].size();

    const std::vector<char> letters = {'M', 'A', 'S'};

    // Loop through vector, check the square as if the point
    // we are at is the top left corner.

    int num_xmas = 0;

    for (int row = 0; row < num_rows - 2; row++) {
        for (int col = 0; col < num_cols - 2; col++) {
            if (input[row][col] != 'M' && input[row][col] != 'S') {
                continue;
            }

            std::string diag_one;
            diag_one = std::string() + input[row][col] + input[row + 1][col + 1] + input[row + 2][col + 2];

            std::string diag_two;
            diag_two = std::string() + input[row + 2][col] + input[row + 1][col + 1] + input[row][col + 2];

            std::cout << diag_one << " " << diag_two << std::endl;

            if (((diag_one == "MAS") or (diag_one == "SAM")) and ((diag_two == "MAS") or (diag_two == "SAM"))) {
                num_xmas++;
            }
        }
    }
    return num_xmas;
}

int main() {
    const bool test = false;
    std::string filename;

    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }

    std::vector<std::string> data = load_data(filename);

    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;
    return 0;
}
