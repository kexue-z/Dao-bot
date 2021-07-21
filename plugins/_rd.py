from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot, Event
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import random

rd = on_command('.rd', aliases={'rd'}, priority=1)

@rd.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await bot.send(event, message=str(random.randint(1,100)))
