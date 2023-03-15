import random

from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.params import Arg, CommandArg, ArgPlainText, EventMessage

jueding = on_command("选择", aliases={"决定"}, priority=1)


@jueding.handle()
async def handle_first_receive(matcher: Matcher, state, arg: Message = CommandArg()):
    args = arg
    # await jueding.send(f"args = {args}")
    if args:
        matcher.set_arg("xuanze", args)


@jueding.got("xuanze", prompt="请输入需要屑岛风bot帮你决定的内容（用空格分开）:")
async def handle_xuanze(xuanze: str = ArgPlainText("xuanze")):
    # await jueding.send(f"xuanze = {xuanze}")
    out = "屑岛风bot认为你应该选择: " + str(random.choice(xuanze.split()))
    await jueding.finish(out)
