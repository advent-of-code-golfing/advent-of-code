#include <fstream>
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <set>

struct InputData {
    std::map<int, std::vector<int> > rules;
    std::vector<std::vector<int> > pages;
};

std::vector<int> split(std::string &s, char delim) {
    std::stringstream ss(s);
    std::string token;
    std::vector<int> tokens;

    while (std::getline(ss, token, delim)) {
        tokens.push_back(std::stoi(token));
    }
    return tokens;
}

InputData load_data(const std::string &filename) {
    std::ifstream file(filename);

    InputData data;
    // map of <int, vector<int>>
    // where the int must appear before all the values in the vector
    std::map<int, std::vector<int> > rules;
    std::vector<std::vector<int> > pages;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return data;
    }

    bool processing_rules = true;
    std::string line;

    while (std::getline(file, line)) {
        if (line.empty()) {
            processing_rules = false;
            continue;
        }
        if (processing_rules) {
            std::vector<int> rule = split(line, '|');
            if (rules.contains(rule[0])) {
                rules[rule[0]].push_back(rule[1]);
            } else {
                rules[rule[0]] = std::vector({rule[1]});
            }
        } else {
            std::vector<int> page = split(line, ',');
            pages.push_back(page);
        }
    }
    data.rules = rules;
    data.pages = pages;
    return data;
}

bool check_page_valid(const std::vector<int> &page, std::map<int, std::vector<int> > &rules) {
    std::set<int> seen = {};
    for (auto num: page) {
        for (auto val: rules[num]) {
            if (seen.contains(val)) {
                // A Number that must appear after this value has already appeared
                return false;
            }
        }
        seen.insert(num);
    }
    return true;
}

int solve_part_one(InputData &data) {
    int total = 0;
    for (int i = 0; i < data.pages.size(); i++) {
        const std::vector<int> &page = data.pages[i];
        if (check_page_valid(page, data.rules)) {
            const int mid_val = page[std::floor(page.size() / 2)];
            total += mid_val;
        }
    }
    return total;
}

bool compare(const int left, const int right, std::map<int, std::vector<int> > rules) {
    // Compares left and right based on the rules.
    // Follows convention based on C++ sort comparator
    // returns true if left > right

    std::vector<int> left_rule = rules[left];
    if (std::ranges::find(left_rule, right) != left_rule.end()) {
        // There is a rule that left must appear before right,
        // i.e. left < right
        return false;
    }
    std::vector<int> right_rule = rules[right];
    if (std::ranges::find(right_rule, left) != right_rule.end()) {
        // There is a rule that right must appear before left
        // i.e. left > right
        return true;
    }
    return false;
}

int solve_part_two(InputData &data) {
    std::map<int, std::vector<int> > rules = data.rules;;
    // Custom comparison function based on the rules
    auto comp = [&rules](const int &a, const int &b) {
        return compare(a, b, rules);
    };
    int total = 0;
    for (int i = 0; i < data.pages.size(); i++) {
        std::vector<int> page = data.pages[i];
        if (check_page_valid(page, data.rules)) {
            continue;
        }
        // Page is not valid - sort into correct order
        std::ranges::sort(page, comp);
        total += page[std::floor(page.size() / 2)];
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
    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;
    return 0;
}
