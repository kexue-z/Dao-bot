from nonebot import on_command
from nonebot.adapters.onebot.v11 import (Bot, Message, MessageEvent,
                                         MessageSegment)
from nonebot.params import CommandArg

from utils.img2b64 import *

from .generator import genImage

sv = on_command("5000choyen", aliases={"5000兆元", "5000兆円", "5kcy"})


@sv.handle()
async def gen_5000_pic(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    keyword = arg.extract_plain_text()
    if not keyword:
        await sv.finish("请提供要生成的句子！")
    if "｜" in keyword:
        keyword = keyword.replace("｜", "|")
    upper = keyword.split("|")[0]
    downer = keyword.split("|")[1]
    img = genImage(word_a=upper, word_b=downer)
    img = img_to_b64(img)
    await sv.finish(MessageSegment.image(img))
