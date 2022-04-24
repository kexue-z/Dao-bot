from pathlib import Path

import yaml

FILE_DIR = Path() / "data" / "mc"


def get_yaml_file(FILE_DIR=FILE_DIR) -> dict:
    FILE = FILE_DIR / "config.yaml"
    if FILE.exists():
        with FILE.open("r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.BaseLoader)
    else:
        data = {"trust_id": [], "server": []}
        FILE_DIR.mkdir()
        with open(FILE, "w+", encoding="utf-8") as f:
            yaml.dump(data, f)
    return data


def get_server_config(server_name) -> dict:
    data = get_yaml_file()
    server = data["server"][server_name]
    return {
        "remote_uuid": server["remote_uuid"],
        "instance_uuid": server["instance_uuid"],
    }


if __name__ == "__main__":
    data = get_yaml_file(FILE_DIR)
    print(data)
    print(data["trust_id"])
