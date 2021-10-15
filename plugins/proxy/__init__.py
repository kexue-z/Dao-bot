import nonebot
from httpx import AsyncClient
from nonebot import logger, on_command
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.permission import SUPERUSER

update_Porxy = on_command("更新订阅", permission=SUPERUSER)

proxy_url = nonebot.get_driver().config.clash_url
docker_url = nonebot.get_driver().config.docker_url


@update_Porxy.handle()
async def _(bot: Bot, event: Event):
    async with AsyncClient() as client:
        res = await client.get(proxy_url)
        with open("./data/clash/config.yaml", "wb") as f:
            f.write(res.content)
    await update_Porxy.send("已保存config.yaml")

    async with AsyncClient() as client:
        url = docker_url + "/containers/clash/restart"
        res = await client.post(url)
    await update_Porxy.send("已重启Clash")
