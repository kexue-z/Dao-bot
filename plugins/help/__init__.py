from nonebot import on_regex
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, Message

message = "[CQ:share,url=https://wiki.kexue.io:3000/,title=屑岛风bot使用指南]"


help = on_regex(r"^(帮助|机器人帮助|机器人说明)$",priority=1)


@help.handle()
async def _(bot: Bot, event: MessageEvent):
    await help.send(message=Message(message))
