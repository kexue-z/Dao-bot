from nonebot import export, on_keyword, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment

test = on_command('kexue', rule=to_me())


@test.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await test.finish(message=MessageSegment.image(file=f'file:////test/test.jpg'))
