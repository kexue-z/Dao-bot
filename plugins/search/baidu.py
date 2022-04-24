from urllib.parse import quote

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg

baidu_url = "https://www.baidu.com/s?wd="

baidu = on_command("百度", aliases={"baidu"}, priority=1)


@baidu.handle()
async def _baidu(args: Message = CommandArg()):
    url = baidu_url + quote(args.extract_plain_text())
    await baidu.finish(message=MessageSegment.text(url))
