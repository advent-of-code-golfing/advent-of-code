#include <fstream>
#include <string>
#include <sstream>
#include <iostream>

struct InputData {
    std:: vector<std::vector<int>> data;
};

InputData load_data() {
    std::ifstream file("../input.txt");

    std::vector<std::vector<int>> data;
    InputData inputData;
    inputData.data = data;


    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return inputData;
    }

    std::string line;
    while (std::getline(file, line)) {
        std::istringstream is(line);
        int val;
        std::vector<int> report;
        while (is >> val) {
            report.push_back(val);
        }
        inputData.data.push_back(report);
    }
    return inputData;
}

bool check_row_safe(const std::vector<int> & row) {
    // Check if a given row is safe
    // A row is safe if:
    // 1. All levels are increasing or all decreasing.
    // 2. Two levels differ by at least one and at most three.
    // For part one at least
    bool increasing = false;
    for (int i = 1; i < row.size(); i++) {
        const int diff = row[i] - row[i - 1];
        // Check greater than 1 and at most 3
        if ((std::abs(diff) < 1) | (std::abs(diff) > 3)) {
            return false;
        }
        // First iteration, set the direction
        if (i == 1) {
            increasing = diff > 0;
        } else {
            // Increasing but direction set to decreasing
            if ((diff > 0 and !increasing) or (diff < 0 and increasing)) {
                return false;
            }
        }
    }
    return true;
}

int solve_part_one(const InputData &inputData) {
    int safe_report_count = 0;
    for (auto & row : inputData.data) {
        if (check_row_safe(row)) {safe_report_count++;}
    }
    return safe_report_count;
}

int solve_part_two(const InputData &inputData) {
    int safe_report_count = 0;
    for (auto & row : inputData.data) {
        if (check_row_safe(row)) {safe_report_count++;}
        else {
            std::vector<int> copy;
            for (int i = 0; i < row.size(); i++) {
                copy = row;
                copy.erase(copy.begin() + i);
                if (check_row_safe(copy)) {
                    safe_report_count++;
                    break;
                }
            }
        }
    }
    return safe_report_count;
}


int main() {
    InputData inputData = load_data();
    std::cout << solve_part_one(inputData) << std::endl;
    std::cout << solve_part_two(inputData) << std::endl;
    return 0;
}
