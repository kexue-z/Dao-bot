from nonebot import on_request, on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent, RequestEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND

super_req = on_request(priority=5)


@super_req.handle()
async def add_superuser(bot: Bot, event: RequestEvent, state: T_State):
    admin = int(list(bot.config.superusers)[0])

    if str(event.user_id) in bot.config.superusers:
        if event.request_type == "private":
            await event.approve(bot)
            await bot.send_private_msg(message=f"添加好友{event.user_id}", user_id=admin)

        elif event.sub_type == "invite" and event.request_type == "group":
            await event.approve(bot)
            await bot.send_private_msg(message=f"添加群{event.group_id}", user_id=admin)

    # elif event.request_type == "invite":
    else:
        # if
        user_name = bot.get_stranger_info(user_id=event.user_id, no_cache=True)
        msg = (
            f"[收到{'好友' if event.request_type == 'friend' else '加群'}邀请]\n"
            f"邀请人: {user_name}({event.user_id})\n"
            f"群: {event.group_id if event.request_type == 'group' else 'n/a'}\n"
        )
        try:
            msg += f"加群请求\n" if event.sub_type == "add" else "邀请入群\n"
        except:
            pass

        admin = int(list(bot.config.superusers)[0])
        msg += f"flag: {event.flag}\n"
        await bot.send_private_msg(user_id=admin, message=msg)


approve_friend = on_command("添加好友", permission=SUPERUSER)


@approve_friend.handle()
async def _(bot: Bot, event: MessageEvent):
    flag = str(event.get_message())
    await bot.set_friend_add_request(flag=flag, approve=True)
    admin = int(list(bot.config.superusers)[0])
    await bot.send_private_msg(message="已添加好友", user_id=admin)


approve_group = on_command("添加群", permission=SUPERUSER)


@approve_group.handle()
async def _(bot: Bot, event: MessageEvent):
    flag = str(event.get_message())
    await bot.set_group_add_request(flag=flag, sub_type="invite", approve=True)
    admin = int(list(bot.config.superusers)[0])
    await bot.send_private_msg(message="已添加群", user_id=admin)
