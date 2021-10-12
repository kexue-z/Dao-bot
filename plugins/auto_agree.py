from nonebot import on_request, on_command, logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, RequestEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from nonebot.adapters.cqhttp.permission import PRIVATE_FRIEND

friend_req = on_request(priority=5)


@friend_req.handle()
async def add_superuser(bot: Bot, event: RequestEvent, state: T_State):
    if str(event.user_id) in bot.config.superusers and event.request_type == "private":
        await event.approve(bot)
        logger.info("add user {}".format(event.user_id))

    elif (
        event.sub_type == "invite"
        and str(event.user_id) in bot.config.superusers
        and event.request_type == "group"
    ):
        await event.approve(bot)
        logger.info("add group {}".format(event.group_id))

    elif event.sub_type == "invite":
        msg = (
            f"[收到{'好友' if event.request_type == 'private' else '加群'}邀请]\n"
            f"邀请人: {event.user_id}\n"
            f"群: {event.group_id}\n"
            f"flag: {event.flag}"
        )
        await bot.send_private_msg(user_id=bot.config.superusers[0], message=msg)

approve_friend = on_command("添加好友",permission=SUPERUSER)

@approve_friend.handle()
async def _(bot: Bot, event: MessageEvent):
    flag = str(event.get_message())
    await bot.set_friend_add_request(flag)
    
approve_group = on_command("添加群",permission=SUPERUSER)

@approve_friend.handle()
async def _(bot: Bot, event: MessageEvent):
    flag = str(event.get_message())
    await bot.set_group_add_request(flag)
    

