#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.onebot.v11 import Adapter
from utils.yaml import Secrets, load_yaml


config = load_yaml("config/config.yaml", Secrets("config"))
nonebot.init(**config)


app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter(Adapter)


nonebot.load_from_toml("pyproject.toml")

if __name__ == "__main__":
    nonebot.run()
