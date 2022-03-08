from nonebot import on_regex

# from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message

message = "[CQ:share,url=https://kexue-z.github.io/Dao-bot/,title=屑岛风bot使用指南]"


help = on_regex(r"^(帮助|机器人帮助|机器人说明)$", priority=1)


@help.handle()
async def _(bot: Bot, event: MessageEvent):
    await help.send(message=Message(message))
