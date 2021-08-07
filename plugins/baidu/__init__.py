from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment

baidu_url = 'https://www.baidu.com/s?ie=utf-8&wd='
bing_url = 'https://www.bing.com/search?q='
sogou_url = 'https://www.sogou.com/web?query='
google_url = 'https://www.google.com/search?q='

baidu = on_command('百度', aliases={'baidu'}, priority=1)
bing = on_command('必应', aliases={'bing'}, priority=1)
sogou = on_command('搜狗', aliases={'sogou'}, priority=1)
google = on_command('谷歌', aliases={'google'}, priority=1)

@baidu.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = baidu_url + event.message
    await baidu.send(message= MessageSegment.share(
        url = msg, 
        title = event.message))

@bing.handle()
async def _(bing: Bot, event: MessageEvent):
    msg = bing_url + event.message
    await bing.send(message= MessageSegment.share(
        url = msg, 
        title = event.message))

@sogou.handle()
async def _(sogou: Bot, event: MessageEvent):
    msg = sogou_url + event.message
    await sogou.send(message= MessageSegment.share(
        url = msg, 
        title = event.message))

@google.handle()
async def _(google: Bot, event: MessageEvent):
    msg = google_url + event.message
    await google.send(message= MessageSegment.share(
        url = msg, 
        title = event.message))