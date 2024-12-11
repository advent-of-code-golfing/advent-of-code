#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <map>

std::vector<long long> split(const std::string &s, char delim) {
    std::stringstream ss(s);
    std::string token;
    std::vector<long long> tokens;

    while (std::getline(ss, token, delim)) {
        tokens.push_back(std::stoll(token));
    }
    return tokens;
}

std::vector<long long> load_data(std::string filename) {
    std::ifstream file(filename);

    std::vector<long long> data;

    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return data;
    }

    std::string line;
    std::getline(file, line);
    data = split(line, ' ');
    return data;
}

size_t num_digits(long long n) {
    std::size_t result = 0;
    while (n) {
        n /= 10;
        result++;
    }
    return result;
}

std::vector<long long> blink(std::vector<long long> data) {
    std::vector<long long> res;

    for (long long val: data) {
        if (val == 0) {
            res.push_back(1);
            continue;
        }
        size_t n = num_digits(val);
        if (n % 2 == 0) {
            // first half
            long div = pow(10, n  / 2);
            res.push_back(std::floor(val / div));
            res.push_back(val % div);
            continue;
        }
        res.push_back(val * 2024);
    }
    return res;
}

long solve_part_one(std::vector<long long> data) {
    std::vector<long long> res;
    for (int i = 0; i < 25; i++) {
        // std::cout << i << std::endl;
        // std::cout << res.size() << std::endl;
        res = blink(data);
        data = res;
    }
    return res.size();
}

long long get_total_after_n_blinks(
    long long val,
    int num_blinks,
    std::map<std::tuple<long long, int>, int>& cache
    ) {
    if (cache.contains(std::make_tuple(val, num_blinks))) {
        return cache.at(std::make_tuple(val, num_blinks));
    }

    // std::cout << num_blinks << std::endl;
    if (num_blinks == 0) {
        return 1;
    }
    if (val == 0) {
        long long res = get_total_after_n_blinks(1, num_blinks - 1, cache);
        std::tuple tup = std::make_tuple(val, num_blinks);
        cache.emplace(tup, res);
        return res;
    }
    size_t n = num_digits(val);
    if (n % 2 == 0) {
        // first half
        long div = pow(10, n  / 2);
        long long first_part = std::floor(val / div);
        long long second_part = val % div;
        long long res_1 = get_total_after_n_blinks(first_part, num_blinks - 1, cache);
        cache.emplace(std::make_tuple(first_part, num_blinks - 1), res_1);

        long long res_2 = get_total_after_n_blinks(second_part, num_blinks - 1, cache);
        cache.emplace(std::make_tuple(second_part, num_blinks - 1), res_2);
        return res_1 + res_2;
    }
    long long res = get_total_after_n_blinks(val * 2024, num_blinks - 1, cache);
    cache.emplace(std::make_tuple(val * 2024, num_blinks - 1), res);
    return res;
}

long long solve_part_two(std::vector<long long> data) {
    long long res = 0;

    std::map<std::tuple<long long, int>, int> cache;

    for (auto val : data) {
        res += get_total_after_n_blinks(val, 75, cache);
    }
    // res = get_total_after_n_blinks(125, 3);
    return res;
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

    std::vector<long long> data = load_data(filename);
    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;

    return 0;
}
