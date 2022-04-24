#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from pathlib import Path

import nonebot
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Adapter

from utils.yaml import Secrets, load_yaml
from utils.pushover import send_startup_message

logger.add(
    "data/log/{time:MM}-{time:DD}.log",
    level="WARNING",
    rotation="1 day",
    compression="zip",
)


config_json = dict(load_yaml("config/config.yaml", Secrets(Path("config"))))  # type: ignore
nonebot.init(**config_json)
send_startup_message(config_json["pushover_token"], config_json["pushover_user"])

app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)


all_plugins = load_yaml("config/plugins.yaml")
nonebot.load_all_plugins(all_plugins["plugins"], all_plugins["plugin_dirs"])  # type: ignore


if __name__ == "__main__":
    nonebot.run()
