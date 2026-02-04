def count_lines(file_path: str) -> int:
    with open(file_path, 'r') as file:
        return sum(1 for _ in file)

if __name__ == 