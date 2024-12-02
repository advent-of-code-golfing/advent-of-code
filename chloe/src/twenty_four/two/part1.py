def main(input_string: str) -> int:
    lines = input_string.split("\n")
    number_of_safe_reports = 0
    for line in lines:
        values = list(map(int, line.split()))

        if not (all(values[j] < values[j+1] for j in range(len(values) - 1)) or 
                  all(values[j] > values[j+1] for j in range(len(values) - 1))):
          continue
      
        is_safe = True
        for i in range(len(values)): 
            if i > 0 and abs(values[i-1] - values[i]) < 1:
                is_safe = False
                break
            if i < len(values) - 1 and abs(values[i] - values[i+1]) > 3:
                is_safe = False
                break
        if is_safe:
            number_of_safe_reports += 1

    return number_of_safe_reports

if __name__ == "__main__":
    file_path = 'input.txt'
    with open(file_path, 'r') as file:
        data = file.read()
    main(data)