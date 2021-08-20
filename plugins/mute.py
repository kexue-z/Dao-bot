from nonebot import on_command
from nonebot.adapters.cqhttp.bot import Bot
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from nonebot.permission import SUPERUSER
from nonebot.adapters.cqhttp.permission import GROUP_OWNER, GROUP_ADMIN

mute_command = on_command(
    '/mute', aliases={'/禁言', '/m'}, priority=1, permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN)


@mute_command.handle()
async def handle_mute(bot: Bot, event: GroupMessageEvent, state: dict):
    raw_args = str(event.get_message()).strip()
    if raw_args:
        arg_list = raw_args.split()
        state["user_id"] = arg_list[0]
        state["time"] = arg_list[1]

    if "CQ:at" in state['user_id']:
        qq_id = state['user_id'][10:-1]
        group_member_info = await bot.get_group_member_info(group_id=event.group_id,
                                                            user_id=qq_id)
        card = group_member_info["card"]
        if card:
            name = card
        else:
            name = group_member_info["nickname"]
        mute_time = int(state['time'])*60
        await bot.set_group_ban(group_id=event.group_id,
                                user_id=qq_id, duration=mute_time)
        await bot.send(event, message=f"{name}被禁言了{state['time']}分钟")

    else:
        await bot.send(event, message="指令错误")

    # get_user_id(raw_args)
