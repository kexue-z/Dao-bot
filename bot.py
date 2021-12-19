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
# nonebot.load_plugin("nonebot_plugin_manager")
nonebot.load_plugin("nonebot_bison")
nonebot.load_plugin("nonebot_plugin_tvseries")
nonebot.load_plugin("nonebot_plugin_heweather")
nonebot.load_plugin("nonebot_plugin_nokia")
# nonebot.load_plugin("nonebot_plugin_setu_now")
# nonebot.load_plugin("nonebot_plugin_picsearcher")
nonebot.load_plugin("nonebot_plugin_trpglogger")
nonebot.load_plugin("nonebot_plugin_status")

if __name__ == "__main__":
    nonebot.run(app="bot:app")
