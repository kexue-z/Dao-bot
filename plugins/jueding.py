from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, GroupMessageEvent
import random

jueding = on_command('选择', aliases={'决定'}, priority=1)


@jueding.handle()
async def handle_first_receive(bot: Bot, event: MessageEvent, state: dict):
    args = str(event.message).strip()
    if args:
        state['xuanze'] = args


@jueding.got('xuanze', prompt='请输入需要屑岛风bot帮你决定的内容（用空格分开）:')
async def handle_xuanze(bot: Bot, event: MessageEvent, state: dict):
    xuanze = state['xuanze']
    out = '屑岛风bot认为你应该选择：'+str(random.choice(xuanze.split()))
    await jueding.finish(out)
