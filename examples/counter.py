def count_lines(file_path: str) -> int:
    with open(file_path, "r") as f:
        return sum(1 for _ in f)


if __name__ == "__main__":
    print(count_lines("examples/sample.py"))
