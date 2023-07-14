import re
from random import randint

from nonebot import on_command
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import CommandArg
from models.mc import UserFrom, MCServers, MCTrustIDs, ServerCommandHistory
from nonebot.adapters.onebot.v11 import Event, Message, MessageEvent, MessageSegment

from ..mcsm import MCSMAPIError, HTTPStatusError, call_server
from ..data_source import server_todo, check_superuser, generate_server_list

mcsm_add = on_command("mcsmadd")
"""QQ: 添加控制服务器的权限"""


@mcsm_add.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    user_id = 0

    user_from = UserFrom.QQ

    if not (
        event.user_id in await MCTrustIDs.get_all_enabled_ids(user_from=user_from)
        or check_superuser(event)
    ):
        await mcsm_add.finish("你没有权限使用这个命令")

    user_list = []

    for msg in arg:
        if msg.type == "at":
            user_list.append(int(msg.data["qq"]))

    if user_id:
        if not await MCTrustIDs.exists(user_id=user_id):
            await MCTrustIDs.add_id(user_id=user_id, user_from=user_from)
            await mcsm_add.finish(
                Message.template("已添加 {}").format(MessageSegment.at(user_id))
            )

    await mcsm_add.finish(Message("添加失败, 或已经存在"))


mcsm_ctl = on_command("mcsm", priority=5)
"""QQ: 开关服务器"""


@mcsm_ctl.handle()
async def _(
    event: MessageEvent,
    state: T_State,
    arg: Message = CommandArg(),
):
    if event.user_id not in await MCTrustIDs.get_all_enabled_ids(user_from=UserFrom.QQ):
        await mcsm_ctl.finish("你没有权限使用这个命令")

    match = re.match(
        r"(on|start|开服|open|off|stop|kill|关服|close|restart|重启|强关|终止)\s?(.*)",
        arg.extract_plain_text(),
    )
    if match:
        state["type"] = server_todo(match.group(1))
        state["code"] = str(randint(10, 99))

        if match.group(2):
            state["server_name"] = match.group(2)
            state["server_id"] = "99"
            logger.debug(f"{state['server_name']}")

        else:
            state["server_name"] = None
            res = await generate_server_list()
            state["list_msg"] = res["list_msg"]
            state["server_list"] = res["server_list"]
    else:
        await mcsm_ctl.finish("使用 mcsm on|off|restart|kill 开启|关闭|重启|强关")


@mcsm_ctl.got("server_id", prompt=Message.template("请输入对应服务器ID:\n{list_msg}"))
async def _(state: T_State):
    logger.debug(f"server_id = {state['server_id']}")
    if str(state["server_id"]) == "0":
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.got("user_code", prompt=Message.template("请输入验证码: {code}"))
async def _(state: T_State):
    if str(state["user_code"]) != state["code"]:
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.handle()
async def _(state: T_State, event: Event):
    try:
        if not state["server_name"]:
            server_name = state["server_list"][int(str(state["server_id"])) - 1]
        else:
            server_name = state["server_name"]

        res = await MCServers.get_server_data(server_name)
        await call_server(state["type"], **res)
        await ServerCommandHistory.add_command_record(
            user_id=int(event.get_user_id()),
            command=state["type"],
            target_instance_uuid=res["instance_uuid"],
            target_remote_uuid=res["remote_uuid"],
            is_success=True,
        )
        await mcsm_ctl.finish(f'已发送 {state["type"]} 指令')

    except HTTPStatusError as e:
        await mcsm_ctl.finish("HTTP错误: " + str(e))

    except MCSMAPIError as e:
        await mcsm_ctl.finish("MCSM API错误: " + str(e))

    except IndexError:
        await mcsm_ctl.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")

    except KeyError:
        await mcsm_ctl.finish("服务器不存在")
