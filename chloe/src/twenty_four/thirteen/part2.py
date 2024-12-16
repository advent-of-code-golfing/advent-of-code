import re

def main(input_string: str) -> int:
    result = 0

    pattern = r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    matches = re.findall(pattern, input_string)

    for match in matches:
        print(f"Match: {match}")
        button_a_x, button_a_y, button_b_x, button_b_y, raw_prize_x, raw_prize_y = map(int, match)
        prize_x = raw_prize_x + 10000000000000
        prize_y = raw_prize_y + 10000000000000

        working_combinations = []
        closest_a_multiple = max(prize_x // button_a_x, prize_y // button_a_y)
        closest_b_multiple = max(prize_x // button_b_x, prize_y // button_b_y)

        det = button_a_x * button_b_y - button_b_x * button_a_y

        if det != 0:
            numerator_i = prize_x * button_b_y - prize_y * button_b_x
            numerator_j = button_a_x * prize_y - button_a_y * prize_x

            if numerator_i % det == 0 and numerator_j % det == 0:
                i = numerator_i // det
                j = numerator_j // det

                if i >= 0 and j >= 0:
                    working_combinations.append({"a": i, "b": j})
                    
        if len(working_combinations) == 0:
            continue

        winning_number_of_tokens = 0
        print(f"Working combinations: {working_combinations}")
        for combo in working_combinations:
            current_number_of_tokens = 3*combo["a"] + combo["b"]

            if (winning_number_of_tokens == 0 or current_number_of_tokens < winning_number_of_tokens):
                winning_number_of_tokens = current_number_of_tokens
        print(f"Winning number of tokens: {winning_number_of_tokens}")
        result += winning_number_of_tokens
            
    print(result)
    return result

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)