from random import randint

from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from nonebot.adapters.cqhttp.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.log import logger
from nonebot.permission import SUPERUSER

dismiss = on_command(
    "dismiss",
    aliases={"退群"},
    priority=1,
    permission=SUPERUSER | GROUP_OWNER | GROUP_ADMIN,
)


@dismiss.handle()
async def d1(bot: Bot, event: GroupMessageEvent, state: dict):
    code = str(randint(10, 99))
    state["code"] = code
    logger.info(f"群:{str(event.group_id)}，请求退群，验证码{code}")
    await dismiss.send(f"确定要退群，输入验证码{code}，或输入0取消")


@dismiss.got("user_code")
async def d2(bot: Bot, event: GroupMessageEvent, state: dict):
    user_code = state["user_code"]
    logger.info(f"验证码:{user_code}")
    if user_code == "0":
        await dismiss.finish()

    user_code = state["user_code"]
    if state["code"] == user_code:
        await bot.set_group_leave(group_id=event.group_id, is_dismiss=True)
    logger.info(f"群：{str(event.group_id)},已退出")
