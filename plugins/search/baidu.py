from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from urllib.parse import quote

baidu_url = 'http://buhuibaidu.me/?s='

baidu = on_command('百度', aliases={'baidu'}, priority=1)

@baidu.handle()
async def _baidu(bot: Bot, event: MessageEvent):
    url = baidu_url + quote(str(event.message))
    # url.replace('&', '&amp;')
    await baidu.send(message = MessageSegment(
        type= 'share', 
        data={'url': url, 
              'title': f'百度{str(event.message)}',
              'content': '你不会百度吗？？？'}
        ))