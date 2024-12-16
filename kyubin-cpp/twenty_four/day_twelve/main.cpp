#include <iostream>
#include <fstream>
#include <deque>
#include <map>
#include <set>
#include <map>



struct Vec {
    int row;
    int col;

    bool operator==(const Vec &rhs) const {
        return row == rhs.row && col == rhs.col;
    }

    Vec operator+(const Vec &rhs) const {
        return Vec{row + rhs.row, col + rhs.col};
    }

    [[nodiscard]] std::tuple<int, int> to_tuple() const {
        return std::make_tuple(row, col);
    }
};

std::vector<Vec> DIRS{
    Vec{1, 0},
    Vec{-1, 0},
    Vec{0, 1},
    Vec{0, -1}
};

class Region {
public:
    std::vector<Vec> points{};
    char value{};

    [[nodiscard]] long area() const {
        return static_cast<int>(points.size());
    }

    [[nodiscard]] long perimeter(int part) const {
        // Essentially a rectangle
        std::vector<int> rows{};
        std::vector<int> cols{};

        std::set<std::tuple<int, int>> borders{};

        // For the border, we will multiply the positions
        // by 2 so each point will have a gap in between.
        // That location of that gap represents the border.
        // i.e. for something at row = 2, col = 2
        // The new position is 4, 4
        // Borders will be placed at
        // (5, 4), (3, 4), (4, 5), (4, 3)

        // The ones in between

        for (auto &vec: points) {
            Vec doubled = Vec{vec.row * 2, vec.col * 2};
            for (auto &dir: DIRS) {
                // If not in borders already
                Vec potential_location = doubled + dir;
                if (!borders.contains(potential_location.to_tuple())){
                    borders.insert(potential_location.to_tuple());
                } else {
                    borders.erase(potential_location.to_tuple());
                }
            }
        }
        // std::cout << value << std::endl;
        // for (auto &vec: borders) {
        //     std::cout << '(' << vec.row << ',' << vec.col << ") ";
        // }
        // std::cout << std::endl;
        if (part == 1) {
            return borders.size();
        }

        std::map<int, std::vector<int>> horizontal_borders{};
        std::map<int, std::vector<int>> vertical_borders{};

        for (auto border: borders) {
            // If first number if odd, horizontal border
            int row = std::get<0>(border);
            int col = std::get<1>(border);

            if (row % 2 == 1) {
                if (horizontal_borders.contains(row)) {
                    horizontal_borders[row].push_back(col);
                } else {
                    horizontal_borders[row] = std::vector<int>{col};
                }
            } else {
                if (vertical_borders.contains(col)) {
                    vertical_borders[col].push_back(row);
                } else {
                    vertical_borders[col] = std::vector<int>{row};
                }
            }
        }

        return 0;
    }
};

class Map {
public:
    std::vector<std::string> map{};
    std::vector<Region> regions{};
    int nrows = 0;
    int ncols = 0;

    explicit Map(const std::vector<std::string> &input) {
        map = input;
        nrows = map.size();
        ncols = map[0].size();
    }

    Map() = default;

    [[nodiscard]] bool within_range(Vec vec) const {
        return vec.row >= 0 && vec.row < nrows && vec.col >= 0 && vec.col < ncols;
    }

    [[nodiscard]] char get_val(Vec vec) const {
        return map[vec.row][vec.col];
    }

    [[nodiscard]] Vec next(Vec vec) const {
        const int next_col = vec.col + 1;
        if (next_col == ncols) {
            return Vec{vec.row + 1, 0};
        } else {
            return Vec{vec.row, next_col};
        }
    }

    [[nodiscard]] long get_total_cost(int part) const {
        long cost = 0;
        for (auto region: regions) {
            cost += region.area() * region.perimeter(part);
            // std::cout << region.value << " - AREA: " << region.area() << " PERIM: "<< region.perimeter() << std::endl;
        }
        return cost;
    }
};

Map load_data(const std::string &filename) {
    std::ifstream file(filename);


    if (!file.is_open()) {
        std::cerr << "Error opening file" << std::endl;
        return Map{};
    }

    std::vector<std::string> data;

    std::string line;
    while (std::getline(file, line)) {
        data.push_back(line);
    }

    Map map = Map{data};
    return map;
}

Region get_region(const Map &map, const Vec start, std::vector<Vec> &included_in_region) {
    Region region{};

    std::deque<Vec> points;
    char letter = map.get_val(start);
    region.value = letter;
    points.push_back(start);

    while (!points.empty()) {
        Vec cur_point = points.front();
        points.pop_front();
        included_in_region.push_back(cur_point);
        region.points.push_back(cur_point);
        for (auto dir: DIRS) {
            Vec next_point = cur_point + dir;
            // Out of range
            if (!map.within_range(next_point)) {
                continue;
            }
            // Already visited
            if (std::ranges::find(included_in_region.begin(), included_in_region.end(), next_point) !=
                included_in_region.end()) {
                continue;
            }
            // In the queue to visit
            if (std::ranges::find(points, next_point) != points.end()) {
                continue;
            }
            if (map.get_val(next_point) == letter) {
                points.push_back(next_point);
            }
        }
    }
    return region;
}

long solve_part_one(Map map) {
    long result = 0;
    std::vector<Vec> included_in_region{};

    Vec cur{0, 0};

    while (map.within_range(cur)) {
        // Skip if this has been visited
        // std::cout << cur.row << ", " << cur.col << std::endl;
        if (std::ranges::find(included_in_region, cur) != included_in_region.end()) {
            cur = map.next(cur);
            continue;
        }
        Region region = get_region(map, cur, included_in_region);
        map.regions.push_back(region);
        cur = map.next(cur);
    }

    long total_cost = map.get_total_cost(1);

    return total_cost;
}

long solve_part_two(Map map) {
    long result = 0;
    std::vector<Vec> included_in_region{};

    Vec cur{0, 0};

    while (map.within_range(cur)) {
        // Skip if this has been visited
        // std::cout << cur.row << ", " << cur.col << std::endl;
        if (std::ranges::find(included_in_region, cur) != included_in_region.end()) {
            cur = map.next(cur);
            continue;
        }
        Region region = get_region(map, cur, included_in_region);
        map.regions.push_back(region);
        cur = map.next(cur);
    }

    long total_cost = map.get_total_cost(2);

    return total_cost;
}

int main() {
    const bool test = true;
    std::string filename;
    if (test) {
        filename = "../input_test.txt";
    } else {
        filename = "../input.txt";
    }

    Map data = load_data(filename);
    std::cout << solve_part_one(data) << std::endl;
    std::cout << solve_part_two(data) << std::endl;
    return 0;
}
