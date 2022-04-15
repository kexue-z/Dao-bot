from nonebot import on_command, on_keyword
from nonebot.rule import to_me

# from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message

message = "[CQ:share,url=https://kexue-z.github.io/Dao-bot/,title=屑岛风bot使用指南]"


help_cmd = on_command("帮助", aliases={"机器人帮助", "机器人说明"}, priority=1)
help_msg = on_keyword({"帮助", "help", "机器人帮助", "机器人说明"}, rule=to_me())


@help_msg.handle()
@help_cmd.handle()
async def _():
    await help.send(message=Message(message))
