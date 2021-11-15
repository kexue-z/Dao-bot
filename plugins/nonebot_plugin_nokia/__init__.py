from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, Message, MessageEvent, MessageSegment
from nonebot.typing import T_State

from .nokia import generate_image

nka = on_regex(r"^(nokia|诺基亚|nka|)(.*)", priority=10)


@nka.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    args = list(state["_matched_groups"])
    msg = args[1]
    b64 = generate_image(msg)
    await nka.finish(MessageSegment.image(b64))
