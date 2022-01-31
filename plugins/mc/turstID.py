import yaml
from pathlib import Path

FILE_DIR = Path() / "data" / "mc"


def get_yaml_file(FILE_DIR=FILE_DIR):
    FILE = FILE_DIR / "config.yaml"
    if FILE.exists():
        with FILE.open("r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
        return data["trust_id"]
    else:
        data = {"trust_id": []}
        FILE_DIR.mkdir()
        with open(FILE, "w+", encoding="utf-8") as f:
            yaml.dump(data, f)


if __name__ == "__main__":
    data = get_yaml_file(FILE_DIR)
    print(data)
