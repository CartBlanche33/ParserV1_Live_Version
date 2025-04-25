import json

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)
