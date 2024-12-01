from pathlib import Path


def get_input_filename(cur_file: str, is_test: bool) -> str:
    dir = Path(cur_file).parent / "input.txt"
    if is_test: 
        dir = Path(cur_file).parent / "input_test.txt"
    
    return dir.__str__()
