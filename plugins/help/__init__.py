from nonebot import on_command, on_keyword
from nonebot.rule import to_me
from nonebot.matcher import Matcher

message = "https://kexue-z.github.io/Dao-bot/"


help_cmd = on_command("帮助", aliases={"机器人帮助", "机器人说明"}, priority=1)
help_msg = on_keyword({"帮助", "help", "机器人帮助", "机器人说明"}, rule=to_me())


@help_msg.handle()
@help_cmd.handle()
async def _(matcher: Matcher):
    await matcher.finish(message=message)
