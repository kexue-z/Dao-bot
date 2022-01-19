import base64

from re import findall

import httpx
from httpx import AsyncClient
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.log import logger

__name__ = "news"
api_url = "https://api.iyk0.com/60s/"


news = on_command("news", aliases={"新闻"}, priority=1)


@news.handle()
async def _(bot: Bot, event: MessageEvent):
    async with AsyncClient() as client:
        try:
            res = await client.get(url=api_url, timeout=10)
            imageUrl = res.json()["imageUrl"]
            logger.debug(imageUrl)
        except Exception as e:
            logger.warning(e)
            await news.finish(f"Error:{e}")
        except httpx.HTTPError as e:
            logger.warning(e)
            await news.finish(f"Error:{e}")

    async with AsyncClient() as client:
        # imageUrl = 'https://img02.sogoucdn.com/app/a/100540022/2021081100125582861289.jpg'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        try:
            re = await client.get(url=imageUrl, headers=headers, timeout=10)
            if re:
                ba = str(base64.b64encode(re.content))
                pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
        except httpx.HTTPError as e:
            logger.warning(e)
            await news.finish(f"Error:{e}")

    await news.finish(MessageSegment.image("base64://" + pic))
