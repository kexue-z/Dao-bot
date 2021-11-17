from io import BytesIO
from typing import Dict

from httpx import AsyncClient
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import (Bot, GroupMessageEvent, Message,
                                     MessageEvent, PrivateMessageEvent)
from nonebot.typing import T_State
from PIL import Image
from pyzbar.pyzbar import decode
from nonebot.log import logger
# from .qr_handle import get_qr_data

# qr_map: Dict[str, str] = {}  # 保存这个群的上一张色图 {"123456":"http://xxx"}


# async def check_qrcode(bot: Bot, event: MessageEvent, state: T_State) -> bool:
#     if isinstance(event, MessageEvent):
#         for msg in event.message:
#             if msg.type == "image":
#                 url: str = msg.data["url"]
#                 state["url"] = url
#                 return True
#         return False


# notice_qrcode = on_message(check_qrcode)


# @notice_qrcode.handle()
# async def handle_pic(bot: Bot, event: GroupMessageEvent, state: T_State):
#     try:
#         group_id: str = str(event.group_id)
#         qr_map.update({group_id: state["url"]})
#     except AttributeError:
#         pass
    

# qrcode = on_command("上一张二维码", aliases={"qrcode"})


qrcode = on_command("qrcode",aliases={"qr","二维码"})

@qrcode.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: T_State):
    msg = event.message
    if msg:
        state["setu"] = msg
    pass

@qrcode.got("qr_img", prompt="图呢")
async def get_qr_img(bot: Bot, event: MessageEvent, state: T_State):
    msg: Message = Message(state["qr_img"])
    # try:
    if msg[0].type == "image":
        url = msg[0].data["url"]
        
        async with AsyncClient() as client:
            res = await client.get(url=url, timeout=10)
        img= Image.open(BytesIO(res.content))
        data = decode(img)
        qr_data = data[0][0]
        logger.info(str(qr_data.decode()))
        await qrcode.finish(str(qr_data.decode()))

