from logging import log
from httpx import AsyncClient
from re import findall
from nonebot import on_command
from nonebot.adapters.cqhttp import(
    Bot, MessageEvent)
from nonebot.adapters.cqhttp.message import MessageSegment
from nonebot.log import logger
import base64
from httpx import AsyncClient


__name__ = 'news'
api_url = 'https://api.iyk0.com/60s/'



news = on_command('news', aliases={'新闻'}, priority=1)

@news.handle()
async def _(bot:Bot, event: MessageEvent):
    logger.info('got')
    async with AsyncClient() as client:
        logger.info('获取图片')
        try:
            res = await client.get(api_url)
            logger.info(res)
            
            imageUrl = res.json()['imageUrl']
            logger.info(imageUrl)
            # with open('./data/news.img')
        except Exception as e:
            logger.warning(e)
            await news.finish(f'Error:{e}')
            
    async with AsyncClient() as client:
        # imageUrl = 'https://img02.sogoucdn.com/app/a/100540022/2021081100125582861289.jpg'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        re = await client.get(url=imageUrl, headers=headers, timeout=10)
        logger.info(type(re))
        if re:
            ba = str(base64.b64encode(re.content))
            pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
            logger.info('成功获取图片')
            
    await news.finish(MessageSegment.image('base64://'+pic))
    