#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

import nonebot
import nonebot.config
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Adapter

from utils.yaml import Secrets, load_yaml
from json import loads

logger.add(
    "data/log/{time:MM}-{time:DD}.log",
    level="WARNING",
    rotation="1 day",
    compression="zip",
)


config = load_yaml("config/config.yaml", Secrets(Path("config")))
nonebot.init(**config)


driver = nonebot.get_driver()
driver.register_adapter(Adapter)


all_plugins = load_yaml("config/plugins.yaml")
nonebot.load_all_plugins(all_plugins["plugins"], all_plugins["plugin_dirs"])  # type: ignore


if __name__ == "__main__":
    nonebot.run()
