#include <fstream>
#include <string>
#include <sstream>
#include <iostream>
#include <map>

struct InputData {
    std:: vector<int> left;
    std:: vector<int> right;
};

InputData load_data() {
    std::ifstream file ("../input.txt");

    std::vector<int> left;
    std::vector<int> right;
    InputData data;
    data.left = left;
    data.right = right;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return data;
    }

    std::string line;
    while (std::getline (file, line)) {
        std::istringstream is (line);
        int x, y;
        is >> x >> y;
        data.left.push_back(x);
        data.right.push_back(y);
    }
    return data;
}

int solve_part_one(InputData data) {
    std::ranges::sort(data.left);
    std::ranges::sort(data.right);

    int sum = 0;

    for (int i = 0; i < data.left.size(); i++) {
        sum = sum + std::abs(data.left[i] - data.right[i]);
    }
    return sum;
}

int solve_part_two(const InputData &data) {
    std::map<int, int> counter;
    for (int key : data.right) {
        if (counter.contains(key)) {
            counter[key]++;
        } else {
            counter[key] = 1;
        }
    }
    int res = 0;

    for (int val : data.left) {
        if (counter.contains(val)) {
            res += val * counter[val];
        }
    }
    return res;
}

int main() {
    const InputData data = load_data();
    int part_one_answer = solve_part_one(data);
    std::cout << part_one_answer << std::endl;

    int part_two_answer = solve_part_two(data);
    std::cout << part_two_answer << std::endl;
    return 0;
}
