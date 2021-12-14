#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot


nonebot.init()


app = nonebot.get_asgi()

driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)


nonebot.load_plugins("plugins")
nonebot.load_plugin("nonebot_plugin_cocdicer")
nonebot.load_plugin("nonebot_plugin_manager")
nonebot.load_plugin("nonebot_bison")


if __name__ == "__main__":
    nonebot.run(app="bot:app")
