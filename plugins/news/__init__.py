from logging import log
from httpx import AsyncClient
from re import findall
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.log import logger
import base64
import httpx


__name__ = "news"
api_url = "https://api.iyk0.com/60s"


news = on_command("news", aliases={"新闻"}, priority=1)


@news.handle()
async def _(bot: Bot, event: MessageEvent):
    # async with AsyncClient() as client:
    #     try:
    #         res = await client.get(url=api_url, timeout=10)
    #         imageUrl = res.json()["imageUrl"]
    #         logger.info(imageUrl)
    #     except Exception as e:
    #         logger.warning(e)
    #         await news.finish(f"Error:{e}")
    #     except httpx.HTTPError as e:
    #         logger.warning(e)
    #         await news.finish(f"Error:{e}")

    # async with AsyncClient() as client:
    #     # imageUrl = 'https://img02.sogoucdn.com/app/a/100540022/2021081100125582861289.jpg'
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
    #         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    #     }
    #     try:
    #         re = await client.get(url=imageUrl, headers=headers, timeout=10)
    #         if re:
    #             ba = str(base64.b64encode(re.content))
    #             pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
    #             logger.info("成功获取图片")
    #     except httpx.HTTPError as e:
    #         logger.warning(e)
    #         await news.finish(f"Error:{e}")

    # await news.finish(MessageSegment.image("base64://" + pic))

    await news.finish("坏了, 改天在修!")
