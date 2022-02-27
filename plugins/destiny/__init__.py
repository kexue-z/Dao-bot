from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.plugin import require
from nonebot_plugin_htmlrender import get_new_page

api_url = "http://www.tianque.top/d2api/today_report/"


ribao = on_command("ribao", aliases={"日报"}, priority=1)
# new_page = require("nonebot_plugin_htmlrender").get_new_page


@ribao.handle()
async def _(bot: Bot, event: MessageEvent):
    async with get_new_page(viewport={"width": 1000, "height": 300}) as page:
        await page.goto(api_url, wait_until="networkidle")
        pic = await page.screenshot(full_page=True)
        await ribao.finish(MessageSegment.image(pic))
