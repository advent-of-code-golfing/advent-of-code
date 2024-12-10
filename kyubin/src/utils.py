from pathlib import Path


def get_input_filename(cur_file: str, test: bool) -> str:
    if test:
        dir = Path(cur_file).parent / "input_test.txt"
    else:
        dir = Path(cur_file).parent / "input.txt"
    return dir.__str__()
