from asyncio import sleep
from io import BytesIO
from typing import Dict

from httpx import AsyncClient
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import ArgPlainText, State
from nonebot.log import logger
from nonebot.typing import T_State
from PIL import Image
from pyzbar.pyzbar import decode

qr_map: Dict[str, str] = {}


async def check_qrcode(bot: Bot, event: MessageEvent, state: T_State = State()) -> bool:
    if isinstance(event, MessageEvent):
        for msg in event.message:
            if msg.type == "image":
                url: str = msg.data["url"]
                state["url"] = url
                return True
        return False


notice_qrcode = on_message(check_qrcode, block=False, priority=90)


@notice_qrcode.handle()
async def handle_pic(bot: Bot, event: MessageEvent, state: T_State = State()):
    if isinstance(event, GroupMessageEvent):
        try:
            group_id: str = str(event.group_id)
            qr_map.update({group_id: state["url"]})
        except AttributeError:
            pass
    elif isinstance(event, PrivateMessageEvent):
        try:
            user_id: str = str(event.user_id)
            qr_map.update({user_id: state["url"]})
        except ArithmeticError:
            pass


pqr = on_command("pqr", aliases={"前一二维码", "pqrcode"})


@pqr.handle()
async def handle_pqr(bot: Bot, event: MessageEvent, state: T_State = State()):
    try:
        url: str = (
            qr_map[str(event.group_id)]
            if isinstance(event, GroupMessageEvent)
            else qr_map[str(event.user_id)]
        )

        async with AsyncClient() as client:
            res = await client.get(url=url, timeout=10)
        img = Image.open(BytesIO(res.content))
        data = decode(img)
        for i in range(len(data)):
            qr_data = data[i][0]
            await pqr.send(str(qr_data.decode()))
            await sleep(3)
        await pqr.finish()
    except (IndexError):
        await pqr.finish()
    except KeyError:
        await pqr.finish("图不对！")


qrcode = on_command("qrcode", aliases={"qr", "二维码"})


@qrcode.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State = State()):
    msg = event.message
    if msg:
        state["qr_img"] = msg
    pass


@qrcode.got("qr_img", prompt="图呢")
async def get_qr_img(bot: Bot, event: MessageEvent, state: T_State = State()):
    msg: Message = Message(state["qr_img"])
    # try:
    if msg[0].type == "image":
        url = msg[0].data["url"]

        async with AsyncClient() as client:
            res = await client.get(url=url, timeout=10)
        img = Image.open(BytesIO(res.content))
        data = decode(img)
        for i in range(len(data)):
            qr_data = data[i][0]
            await qrcode.send(str(qr_data.decode()))
            await sleep(3)
        await qrcode.finish()
    else:
        await qrcode.finish("这啥？指令已取消")
