from PIL import Image

# from hoshino import Service, priv, logger, aiorequests
# from hoshino.typing import CQEvent, MessageSegment
# from hoshino.util import FreqLimiter, DailyNumberLimiter, pic2b64

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from utils.img2b64 import *

from .generator import genImage

# lmt = DailyNumberLimiter(10)

sv = on_command("5000choyen", aliases={"5000兆元", "5000兆円", "5kcy"})


@sv.handle()
async def gen_5000_pic(bot: Bot, event: MessageEvent):
    # uid = event.user_id
    # gid = event.group_id
    # mid = event.message_id
    # if not lmt.check(uid):
    #     await bot.send(ev, f'您今天已经使用过10次生成器了，休息一下明天再来吧~', at_sender=True)
    #     return
    try:
        keyword = event.message.extract_plain_text().strip()
        if not keyword:
            await bot.send(event, "请提供要生成的句子！")
            return
        if "｜" in keyword:
            keyword = keyword.replace("｜", "|")
        upper = keyword.split("|")[0]
        downer = keyword.split("|")[1]
        img = genImage(word_a=upper, word_b=downer)
        img = str(MessageSegment.image(img_to_b64(img)))
        await bot.send(event, img)
        # lmt.increase(uid)
    except OSError as e:
        await bot.send(event, f"生成失败……请检查字体文件设置是否正确{e}")
    except:
        await bot.send(event, "生成失败……请检查命令格式是否正确")
