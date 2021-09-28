import base64
from io import BytesIO

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, MessageSegment
from nonebot.typing import T_State
from PIL import Image

from .logo import make_logo

phlogo = on_command("phlogo", aliases={"pornhub", "ph图标"})


def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str


@phlogo.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = str(event.get_message()).split()
    if len(msg) == 2:
        pic = img_to_b64(make_logo(msg[0], msg[1]))
        await phlogo.finish(MessageSegment.image(pic))
    else:
        await phlogo.finish("请输入正确的参数,用空格分开")
