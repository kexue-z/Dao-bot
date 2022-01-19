from time import sleep
from nonebot import on_notice, get_driver
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import GroupBanNoticeEvent, Event

group_mute = on_notice(priority=10, block=True)


@group_mute.handle()
async def sent_mute(bot: Bot, event: GroupBanNoticeEvent):
    group_id = event.group_id
    qq_id = event.user_id
    mute_time = event.duration
    group_info = await bot.get_group_info(group_id=event.group_id)
    group_name = group_info["group_name"]
    operator_id = event.operator_id
    # 获取被禁言人名字
    mute_member_info = await bot.get_group_member_info(group_id=group_id, user_id=qq_id)
    if mute_member_info["card"]:
        mute_name = mute_member_info["card"]
    else:
        mute_name = mute_member_info["nickname"]
    # 获取管理人名字
    operator_member_info = await bot.get_group_member_info(
        group_id=group_id, user_id=operator_id
    )
    if operator_member_info["card"]:
        operator_name = operator_member_info["card"]
    else:
        operator_name = operator_member_info["nickname"]

    if mute_member_info["user_id"] == event.self_id and mute_time:
        # 被禁言提示
        message = f"Bot在群{event.group_id}（{group_name}）被 {operator_name} 禁言了 {mute_time//60} 分钟"
        await bot.send_private_msg(
            user_id=list(get_driver().config.superusers)[0], message=message
        )

    elif mute_time:
        message = f"{mute_name} 被 {operator_name} 禁言了 {mute_time//60} 分钟!"
        await bot.send(event, message)

    elif mute_time == 0:
        if mute_member_info["user_id"] == event.self_id:
            message = f"Bot在群{event.group_id}（{group_name}）的禁言被 {operator_name} 解除了！"
            await bot.send_private_msg(
                user_id=list(get_driver().config.superusers)[0], message=message
            )
            sleep(5)
        message = f"{mute_name} 被 {operator_name} 复活了!"
        await bot.send(event, message)
