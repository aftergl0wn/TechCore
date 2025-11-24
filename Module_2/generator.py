def read_large_log(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for value in f:
            yield value.strip()


if __name__ == "__main__":
    generator = read_large_log("text.txt")
    print(next(generator))
    print(next(generator))
    print(next(generator))
    print(next(generator))
