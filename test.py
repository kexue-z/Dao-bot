from utils.yaml import Secrets, load_yaml
from pathlib import Path


config = load_yaml("config/config.yaml", Secrets(Path("config")))

print(config)
print(type(config))
print((config.keys()))
print(type(config.keys()))
