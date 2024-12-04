#include <fstream>
#include <iostream>
#include <regex>

std::string load_data() {
    std::ifstream file("../input.txt");

    std::string res;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return res;
    }

    std::string line;

    while (std::getline(file, line)) {
        res += line;
    }
    return res;
}

int solve_part_one(std::string &input) {
    std::regex pattern(R"(mul\((\d{1,3}),(\d{1,3})\))");
    auto begin = std::sregex_iterator(input.begin(), input.end(), pattern);
    auto end = std::sregex_iterator();

    int total = 0;

    for (auto it = begin; it != end; ++it) {
        const std::smatch &match = *it;
        int num1 = std::stoi(match[1].str());
        int num2 = std::stoi(match[2].str());
        total += num1 * num2;
    }
    return total;
}

int solve_part_two(std::string &input) {
    std::regex pattern(R"((don't)|(do)|mul\((\d{1,3}),(\d{1,3})\))");
    auto begin = std::sregex_iterator(input.begin(), input.end(), pattern);
    auto end = std::sregex_iterator();

    int total = 0;
    bool do_next = true;

    for (std::regex_iterator it = begin; it != end; ++it) {
        const std::smatch &match = *it;

        if (match[1].str() == "don't") {
            do_next = false;
            continue;
        }
        if (match[2].str() == "do") {
            do_next = true;
            continue;
        }

        if (do_next) {
            int num1 = std::stoi(match[3].str());
            int num2 = std::stoi(match[4].str());
            total += num1 * num2;
        }
    }
    return total;
}


int main() {
    std::string input = load_data();
    std::cout << solve_part_one(input) << std::endl;
    std::cout << solve_part_two(input) << std::endl;
    return 0;
}
