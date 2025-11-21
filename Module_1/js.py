import json

dict_value = {
    "name": "Алиса",
    "year": 2020,
    "message": "Hi",
}

with open("config.json", "w", encoding="utf-8") as f:
    json.dump(dict_value, f, indent=4, ensure_ascii=False)

with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data)
