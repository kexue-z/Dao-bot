from json import loads
from random import choice
from time import localtime, strftime

from anyio import open_file
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageSegment, escape
from nonebot.params import CommandArg

# from nonebot.utils import unescape
fabing = on_command("fabing", aliases={"发病"})


@fabing.handle()
async def _(args: Message = CommandArg()):
    text = []
    async with await open_file("./data/bing.json") as f:
        # contents = await f.read()
        f = await f.read()
        f = loads(f)
        for i in f["data"]:
            if i != "\n":
                text.append(i)
    c_text = choice(text)

    date_str = strftime("%Y年%m月%d日", localtime())
    msg = Message.template(c_text).format(name=args.extract_plain_text(), date=date_str)

    await fabing.finish(msg)
