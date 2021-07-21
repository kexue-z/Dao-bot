from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import MessageEvent, Message

message = "[CQ:share,url=https://www.notion.so/kexue/bot-cded534e8aa3434298e63399d6952751,title=屑岛风bot使用指南]"


help = on_command('帮助',
                  aliases={'机器人帮助', '机器人说明'}, 
                  priority=1)

@help.handle()
async def _(bot: Bot, event:MessageEvent):
    await help.send(message=Message(message))