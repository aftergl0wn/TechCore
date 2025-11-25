import json


def write_file(dict_value, file):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(dict_value, f, indent=4, ensure_ascii=False)


def read_file(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    dict_value = {
        "name": "Алиса",
        "year": 2020,
        "message": "Hi",
    }
    write_file(dict_value, "config.json")
    data = read_file("config.json")
    print(data)
