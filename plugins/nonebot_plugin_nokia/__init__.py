from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Message, MessageEvent, MessageSegment
from nonebot.typing import T_State

from .nokia import generate_image

nka = on_command("nokia",aliases={"nka","诺基亚"}, priority=10)


@nka.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message())
    b64 = generate_image(msg)
    await nka.finish(MessageSegment.image(b64))
