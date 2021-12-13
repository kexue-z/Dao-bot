import base64
from io import BytesIO
from .date_source import get_tvseries
from nonebot import on_command, on_message
from nonebot.adapters.cqhttp import Bot, Event, MessageEvent, MessageSegment
from PIL import Image

def img_to_b64(pic: Image.Image) -> str:
    buf = BytesIO()
    pic.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getbuffer()).decode()
    return "base64://" + base64_str

tvseries = on_command("美剧", aliases={"tvseries"})

@tvseries.handle()
async def _(bot: Bot, event: MessageEvent):
    pic_raw = get_tvseries()
    await tvseries.finish(img_to_b64(pic_raw))
    