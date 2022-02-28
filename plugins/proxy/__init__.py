import nonebot
from httpx import AsyncClient
from nonebot import logger, on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.params import ArgPlainText, State
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .data_source import *

update_Porxy = on_command("更新订阅", permission=SUPERUSER)

proxy_url = nonebot.get_driver().config.proxy_url
docker_url = nonebot.get_driver().config.docker_url
clash_url = nonebot.get_driver().config.clash_url


@update_Porxy.handle()
async def _(bot: Bot, event: Event):
    async with AsyncClient() as client:
        res = await client.get(clash_url)
        with open("./data/clash/config.yaml", "wb") as f:
            f.write(res.content)
    await update_Porxy.send("已保存config.yaml")

    async with AsyncClient() as client:
        url = docker_url + "containers/clash/restart"
        res = await client.post(url)
        if res.status_code == 204:
            await update_Porxy.send("已重启Clash")
        else:
            await update_Porxy.send(f"错误! {res.status_code}")


get_Proxy = on_command("订阅选择", permission=SUPERUSER)


@get_Proxy.handle()
async def get_Proxy_list(bot: Bot, event: Event, state: T_State = State()):
    args = str(event.get_message()).split()

    proxies = await get_Proxies(proxy_url)
    state["proxies"] = proxies

    if "ping" in args:
        await get_Proxy.send("正在获取延迟...")
        delay_list = await get_Proxies_delay(proxies, proxy_url, 2000)
        data = []
        for i in range(len(proxies)):
            data.append(f"{proxies[i]} Ping: {delay_list[i]}")
            msg = "\n".join([f"{i}: {line} " for i, line in enumerate(data, start=1)])
            msg += "\n输入ID来选择"
    else:
        msg = "\n".join([f"{i}: {line} " for i, line in enumerate(proxies, start=1)])
        msg += "\n输入ID来选择"
    await get_Proxy.send(msg)


@get_Proxy.got("Selection")
async def get_Proxy_Selection(bot: Bot, state: T_State = State()):
    pass


@get_Proxy.handle()
async def get_Proxy_done(bot: Bot, state: T_State = State()):
    user_Selection = int(state["Selection"].extract_plain_text()) - 1
    if user_Selection == -1:
        await get_Proxy.finish("已取消")
    Selection = state["proxies"][user_Selection]
    logger.info(f"已选择节点 {Selection}")
    res = await Select_Proxy(Selection, proxy_url)
    if res == 204:
        await get_Proxy.finish(f"已选择节点 {Selection}")
    else:
        logger.error(f"已选择节点 {Selection}")
        await get_Proxy.finish(f"错误! {res}")
