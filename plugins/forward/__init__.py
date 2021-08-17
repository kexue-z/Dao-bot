from nonebot import on_command, on_message
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message, GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
import nonebot


forward = on_message(priority=99, rule=to_me())


@forward.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = event.message
    uid = event.user_id
    superusers = nonebot.get_driver().config.superusers
    if event.get_user_id() in superusers:
        await forward.finish()
    if isinstance(event, GroupMessageEvent):
        info = await bot.get_group_member_info(group_id=event.group_id,
                                               user_id=uid)
        group_info = await bot.get_group_info(group_id=event.group_id)
        group_name = group_info["group_name"]
        if info["card"]:
            name = info["card"]
        else:
            name = info["nickname"]
        for superuser in superusers:
            await bot.send_msg(user_id=superuser,
                               message=Message(
                                   f'群 {group_name}({event.group_id}) | {name}({uid}):\n{msg}'
                               ))
    else:
        info = await bot.get_stranger_info(user_id=uid)
        for superuser in superusers:
            await bot.send_msg(user_id=superuser,
                               message=Message(f'{info["nickname"]}({uid}):\n{msg}'))
