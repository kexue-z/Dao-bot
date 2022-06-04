from urllib.parse import quote

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.params import CommandArg

geng_url = "https://jikipedia.com/search?phrase="

geng = on_command("梗", aliases={"geng"}, priority=1)


@geng.handle()
async def _geng(args: Message = CommandArg()):
    url = geng_url + quote(args.extract_plain_text())
    await geng.finish(message=MessageSegment.text(url))
