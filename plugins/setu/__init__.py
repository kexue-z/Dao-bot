import json
import re
import random

import nonebot
from nonebot import on_command
from nonebot.adapters.cqhttp import (
    Bot,
    Message,
    GroupMessageEvent,
    Event,
    PrivateMessageEvent,
)
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND, GROUP
from nonebot.log import logger

from .getPic import ghs_pic3
from .setu_Message import *

__name__ = "setu"

setu = on_command(
    "setu",
    aliases={"无内鬼", "涩图", "色图", "来点色色", "色色"},
    permission=PRIVATE_FRIEND | GROUP,
)
withdraw = on_command("撤回")
cdTime = nonebot.get_driver().config.cdtime
data_dir = r"./data/setuCD/"


@setu.handle()
async def _(bot: Bot, event: Event):
    global mid
    qid = event.get_user_id()
    mid = event.message_id
    data = readJson()
    try:
        cd = event.time - data[qid][0]
    except:
        cd = cdTime + 1

    args = str(event.get_message()).split()
    r18 = True if (isinstance(event, PrivateMessageEvent) and "r18" in args) else False

    if r18:
        args.remove("r18")
    try:
        key = " ".join(args) if args is not None else ""
    except:
        key = ""

    logger.info(f"key={key},r18={r18}")

    # try:
    if cd > cdTime or event.get_user_id() in nonebot.get_driver().config.superusers:
        # await setu.send(random.choice(setu_SendMessage), at_sender=True)
        writeJson(qid, event.time, mid, data)
        pic = await ghs_pic3(key, r18)
        if pic[2]:
            try:
                await setu.send(message=Message(pic[0]))
                logger.info("已发送")
                await setu.send(
                    message=f"{random.choice(setu_SendMessage)}\n" + Message(pic[1]),
                    at_sender=True,
                )
                # writeJson(qid, event.time, mid['message_id'], data)
            except Exception as e:
                logger.warning(e)
                removeJson(qid)
                await setu.finish(
                    message=Message(f"消息被风控，图发不出来\n{pic[1]}\n这是链接\n{pic[3]}"),
                    at_sender=True,
                )

        else:
            removeJson(qid)
            await setu.finish(pic[0] + pic[1])

    else:
        await setu.send(
            f"{random.choice(setu_SendCD)} 你的CD还有{cdTime - cd}秒", at_sender=True
        )


def readJson():
    try:
        with open(data_dir + "usercd.json", "r") as f_in:
            data = json.load(f_in)
            f_in.close()
            return data
    except FileNotFoundError:
        try:
            import os

            os.makedirs(data_dir)
        except FileExistsError:
            pass
        with open(data_dir + "usercd.json", mode="w") as f_out:
            json.dump({}, f_out)


def writeJson(qid: str, time: int, mid: int, data: dict):
    data[qid] = [time, mid]
    with open(data_dir + "usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()


def removeJson(qid: str):
    with open(data_dir + "usercd.json", "r") as f_in:
        data = json.load(f_in)
        f_in.close()
    data.pop(qid)
    with open(data_dir + "usercd.json", "w") as f_out:
        json.dump(data, f_out)
        f_out.close()
