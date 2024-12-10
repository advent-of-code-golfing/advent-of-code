#include <deque>
#include <iostream>
#include <fstream>

std::string load_data(std::string& filename) {
    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return std::string{};
    }

    std::string line;

    std::getline(file, line);
    return line;
}

struct Mem {
    int occ{};
    int val{};
};

long solve_part_one(std::string& input) {
    std::deque<int> queue;
    // Even indices are filled, odd indices are empty
    // ID for filled is index / 2
    for (int i = 0; i < input.size(); i++) {
        int to_fill;
        if (i % 2 == 0) {
            to_fill = i / 2;
        } else {
            to_fill = -1;
        }
        const int iterations = input[i] - '0';
        for (int j = 0; j < iterations; j++) {
            queue.push_back(to_fill);
        }
    }
    // for (int i : queue) {
    //     std::cout << i << " ";
    // }
    // std::cout << std::endl;

    long res = 0;
    int i = 0;

    while (!queue.empty()) {
        int cur = queue.front();
        queue.pop_front();
        if (cur == -1) {
            while (!queue.empty()) {
                const int end_val = queue.back();
                queue.pop_back();
                if (end_val == -1) {continue;}
                res += i * end_val;
                break;
            }
        } else {
            res += i * cur;
        }
        i++;
    }
    return res;
}

void print_memory(std::vector<Mem>& memory) {
    for (auto mem: memory) {
        for (int i = 0; i < mem.occ; i++) {
            if (mem.val == -1) {
                std::cout << '.';
            } else {
                std::cout << mem.val;
            }
        }
    }
    std::cout << std::endl;
}

long sum_values(std::vector<Mem>& memory) {
    long total = 0;
    int j = 0;
    for (auto mem: memory) {
        for (int i = 0; i < mem.occ; i++) {
            if (mem.val == -1) {
                j++;
            } else {
                total += mem.val * j;
                j++;
            }
        }
    }
    return total;
}

std::vector<Mem> fit_into_string(std::vector<Mem>& input, Mem to_add) {
    int n = input.size();
    for (int i = 0; i < n; i++) {
        Mem cur = input[i];
        if (cur.val == to_add.val) {
            break;
        }

        if (cur.val != -1) {
            continue;
        }
        if (cur.occ >= to_add.occ) {
            input[i].occ -= to_add.occ;
            input.insert(input.begin() + i, to_add);
            // Remove this from the list
            for (int j = i + 1; j < input.size(); j++) {
                // This is a big disgusting but oh well
                if (input[j].val == to_add.val) {
                    // input.erase(input.begin() + j, input.begin() + j + 1);
                    input[j].val = -1;
                    break;
                }
            }
            break;
        }
    }

    // print_memory(input);
    return input;
}

long solve_part_two(std::string& input) {
    // Change the string into format:
    // 2333133121414131402 ->
    // {(2, 0), (3, .), ...}
    // -> 2 zeros, 3 dot, 3 ones, 3 dots, 1 two, 3 dots, etc

    std::vector<Mem> memory;
    std::string modified{};
    std::vector<int> non_empty;

    for (int i = 0; i < input.size(); i++) {
        int to_fill;
        if (i % 2 == 0) {
            int id = i / 2;
            memory.push_back(Mem{input[i] - '0', id});
            non_empty.push_back(input[i] - '0');
        } else {
            memory.push_back(Mem{input[i] - '0', -1});
        }
    }

    for (int i = 0; i < non_empty.size(); i++) {
        std::cout << non_empty[i];
    }
    // Starting from back, fit non-empty elements into string
    std::cout << std::endl;
    // print_memory(memory);

    for (int i = non_empty.size() - 1; i >= 0; i--) {
        Mem cur = Mem{static_cast<int>(non_empty[i]), i};
        // std::cout << cur.occ << " " << cur.val << std::endl;
        memory = fit_into_string(memory, cur);
    }
    // print_memory(memory);

    return sum_values(memory);
}

int main()
{
    const bool test = false;
    std::string filename;
    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }
    std::string input = load_data(filename);
    std::cout << solve_part_one(input) << std::endl;
    std::cout << solve_part_two(input) << std::endl;
    return 0;
}
