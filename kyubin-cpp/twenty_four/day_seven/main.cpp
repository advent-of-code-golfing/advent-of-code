#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>

struct InputData {
    std::vector<long long> results{};
    std::vector<std::vector<long long> > operations{};
};

std::vector<std::string> split(const std::string &s, char delim) {
    std::stringstream ss(s);
    std::string token;
    std::vector<std::string> tokens;

    while (std::getline(ss, token, delim)) {
        tokens.push_back(token);
    }
    return tokens;
}

InputData load_data(const std::string &filename) {
    std::ifstream file(filename);

    InputData data;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return data;
    }

    std::string line;

    while (std::getline(file, line)) {
        std::vector<std::string> tokens = split(line, ':');
        data.results.push_back(std::stoll(tokens[0]));
        std::vector<std::string> operations = split(tokens[1], ' ');
        std::vector<long long> operations_int;
        for (int i = 0; i < operations.size(); ++i) {
            if (operations[i] == "") { continue; }
            operations_int.push_back(std::stoll(operations[i]));
        }
        data.operations.push_back(operations_int);
    }
    return data;
}

long get_operations_results(std::vector<long long> numbers, int operations) {
    long result = numbers[0];
    for (int i = 1; i < numbers.size(); i++) {
        int bit = operations & 1;
        if (bit == 1) {
            result += numbers[i];
        } else {
            result *= numbers[i];
        }
        operations >>= 1;
    }
    return result;
}

long solve_part_one(InputData &data) {
    // Try all combinations using binary
    // 1 is add, 0 is multiply
    long total = 0;

    for (int i = 0; i < data.results.size(); ++i) {
        int bits = pow(2, (data.operations[i].size()) - 1) - 1;
        // std::cout << "Trying to solve " << bits << " bits" << std::endl;
        while (bits >= 0) {
            long res = get_operations_results(data.operations[i], bits);
            if (res == data.results[i]) {
                std::cout << "BITS: " << bits << " RES: " << res << std::endl;
                total += res;
                break;
            }
            bits--;
        }
    }
    return total;
}

std::string to_base_three(long long val, int min_digits) {
    std::string base;

    while (min_digits > 0) {
        base = std::to_string(val % 3) + base;
        val = val / 3;
        min_digits--;
    }
    return base;
}

long long get_operations_results_part_two(const std::vector<long long>& numbers, const std::string& operations) {
    long long result = numbers[0];
    // std::string operations_string = to_base_three(operations);
    // 1: add, 2: string combine, 0: multiply

    if (numbers.size() - 1 != operations.size()) {
        std::cerr << "Error in get_operations_results_part_two" << std::endl;
    }

    for (int i = 1; i < numbers.size(); i++) {
        if (operations[i - 1] == '2') {
            std::string combined_string = std::to_string(result) + std::to_string(numbers[i]);
            result = std::stoll(combined_string);
        } else if (operations[i - 1] == '1') {
            result += numbers[i];
        } else if (operations[i - 1] == '0') {
            result *= numbers[i];
        }
    }
    return result;
}

long solve_part_two(InputData data) {
    // Try all combinations using binary
    // 1 is add, 0 is multiply
    long total = 0;

    for (int i = 0; i < data.results.size(); ++i) {
        int bits = pow(3, (data.operations[i].size()) - 1) - 1;
        int min_digits = data.operations[i].size() - 1;

        // std::cout << "Trying to solve " << bits << " bits" << std::endl;
        while (bits >= 0) {
            std::string operations = to_base_three(bits, min_digits);
            long res = get_operations_results_part_two(data.operations[i], operations);
            // std::cout << "I: " << i << " RES: " << res << " OPS: " << operations << std::endl;
            if (res == data.results[i]) {
                // std::cout << "BITS: " << bits << " RES: " << res << std::endl;
                total += res;
                break;
            }
            bits--;
        }
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
    InputData data = load_data(filename);
    // std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;

    return 0;
}
