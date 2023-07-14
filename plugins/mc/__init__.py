from nonebot import require

require("nonebot_plugin_tortoise_orm")
require("nonebot_plugin_htmlrender")
require("nonebot_plugin_apscheduler")

from nonebot_plugin_htmlrender import md_to_pic
from nonebot_plugin_tortoise_orm import add_model

add_model("models.mc")

from typing import Set
from random import randint

from nonebot.rule import Rule
from nonebot import get_driver
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.plugin import on_command
from nonebot.adapters import Event, Message
from nonebot.params import Depends, CommandArg
from nonebot.adapters.kaiheila import Event as KEvent
from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.adapters.kaiheila import Message as KMessage
from nonebot.adapters.kaiheila import MessageSegment as KMS
from nonebot.adapters.onebot.v11 import Message as V11Message
from nonebot.adapters.onebot.v11 import MessageEvent as V11MessageEvent
from models.mc import UserFrom, MCServers, MCTrustIDs, ServerCommandHistory

from .qq import mcsm_add, mcsm_ctl
from .kook import kmcsm, kmcsm_add, kmcsm_button
from .mcsm import MCSMAPIError, HTTPStatusError, call_command
from .data_source import mc_ping_qq, mc_ping_kook, generate_server_list

superusers = get_driver().config.superusers
kook_superusers: Set[str] = get_driver().config.kook_superusers


mc_server = on_command("mc", priority=1)
"""QQ/KOOK: 获取MC服务器状态"""


@mc_server.handle()
async def _(event: Event):
    if isinstance(event, KEvent):
        card = await mc_ping_kook()
        await mc_server.send(KMessage(KMS.Card(card)))

    elif isinstance(event, V11MessageEvent):
        msg = await mc_ping_qq()
        pic = await md_to_pic(msg)
        await mc_server.send(MessageSegment.image(pic))

    await mc_server.finish()


async def is_in_white_list(
    event: V11MessageEvent | KEvent,
    state: T_State,
):
    if isinstance(event, V11MessageEvent):
        user_from = UserFrom.QQ

    else:
        user_from = UserFrom.Kook

    user_id = int(event.user_id)

    if user_id in await MCTrustIDs.get_all_enabled_ids(user_from=user_from):
        state["user_id"] = user_id
        state["user_from"] = user_from
        return True

    if str(user_id) in superusers or str(user_id) in kook_superusers:
        return True

    return False


def check_command(state: T_State, args: V11Message | KMessage = CommandArg()):
    if isinstance(args, V11Message):
        command = args.extract_plain_text()

    elif isinstance(args, KMessage):
        command = args.extract_plain_text()

    state["command"] = command


mcsm_command = on_command("mcc", rule=Rule(is_in_white_list))
"""双端通用: MC 执行指令"""


@mcsm_command.handle(parameterless=[Depends(check_command)])
async def _(state: T_State):
    command: str = state["command"]
    if command.startswith("/"):
        await mcsm_command.finish("不需要 / , 重新执行指令")

    if command.strip() != "":
        state["command"] = command

    # 生成列表
    res = await generate_server_list()
    state["list_msg"] = res["list_msg"]
    state["server_list"] = res["server_list"]

    # 生成验证码
    state["code"] = str(randint(10, 99))


@mcsm_command.got("command", prompt="请输出你要执行的指令, 不需要 /")
async def _():
    pass


@mcsm_command.got("server_id", prompt=Message.template("请输入对应服务器ID:\n{list_msg}"))
async def _(state: T_State):
    if str(state["server_id"]) == "0":
        await mcsm_command.finish("已取消")


@mcsm_command.got("user_code", prompt=Message.template("请输入验证码: {code}"))
async def _(state: T_State):
    if str(state["user_code"]) != state["code"]:
        await mcsm_command.finish("已取消")


@mcsm_command.handle()
async def _(state: T_State):
    logger.debug(state)
    try:
        server_name = state["server_list"][int(str(state["server_id"])) - 1]

        server_data = await MCServers.get_server_data(server_name)

        await call_command(command=state["command"], **server_data)

        await ServerCommandHistory.add_command_record(
            command=state["command"],
            user_id=state["user_id"],
            target_instance_uuid=server_data["instance_uuid"],
            target_remote_uuid=server_data["remote_uuid"],
            is_success=True,
        )

        await mcsm_command.finish("执行成功")

    except HTTPStatusError as e:
        await mcsm_command.finish("HTTP错误: " + str(e))

    except MCSMAPIError as e:
        await mcsm_command.finish("MCSM API错误: " + str(e))

    except IndexError:
        await mcsm_command.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")

    except KeyError:
        await mcsm_command.finish("服务器不存在")


# mcsm_command_history = on_command("命令历史")
# """双端通用: 命令历史"""


# @mcsm_command_history.handle()
# async def _(
#     bot: Bot, event: GroupMessageEvent | MessageEvent, args: Message = CommandArg()
# ):
#     user_id = None

#     if isinstance(event, GroupMessageEvent):
#         for a in args:
#             if a.type == "at":
#                 user_id = int(a.data["qq"])
#                 break

#     res = await ServerCommandHistory.get_recent_history(user_id=user_id)

#     text = "# 命令执行历史\n\n"

#     for i in res:
#         user_info = await bot.get_stranger_info(user_id=i.user_id)
#         nickname = "{}({})".format(user_info["nickname"], user_info["user_id"])
#         # nickname = "123"
#         server_name = await MCServers.get_server_name_by_uuid(i.target_instance_uuid)
#         text += (
#             f"- {nickname}\n"
#             f"\t - 目标服务器: `{server_name}`\n"
#             f"\t - 指令: `{i.command.strip()}`\n"
#             f"\t - 时间: `{i.time.astimezone(tz.tzlocal()).strftime('%m/%d, %H:%M:%S')}`\n"
#         )

#     await mcsm_command_history.finish(MessageSegment.image(await md_to_pic(text)))

mcadd = on_command("mcadd", rule=Rule(is_in_white_list))
"""双端通用: 添加MC服务器"""


# @mcadd.handle(parameterless=[Depends(check_command)])
# async def _(state: T_State):
#     name = args.extract_plain_text()
#     if name.strip() != "":
#         state["name"] = name


@mcadd.got("name", prompt="请输入名称", parameterless=[Depends(check_command)])
async def _(state: T_State):
    if await MCServers.exists(name=state["name"]):
        await mcadd.finish("名称 {name} 已存在, 换一个别的或者删除它")


@mcadd.got("uuid", prompt="输入实例UUID")
async def _():
    pass


@mcadd.got("remote_uuid", prompt="输入服务器UUID")
async def _():
    pass


@mcadd.got("ip", prompt="输入服务器IP")
async def _():
    pass


@mcadd.handle()
async def _(state: T_State):
    logger.info(state)
    res = await MCServers.add_server(
        name=state["name"],
        instance_uuid=state["uuid"],
        remote_uuid=state["remote_uuid"],
        ip=state["ip"],
    )
    if res:
        await mcadd.finish(f'服务器已添加 {state["name"]}: {state["ip"]}')


mcdel = on_command("mcdel", rule=Rule(is_in_white_list))
"""双端: 删除服务器"""


@mcdel.handle()
async def _(state: T_State):
    res = await generate_server_list()
    state["list_msg"] = res["list_msg"]
    state["server_list"] = res["server_list"]


@mcdel.got("server_id", prompt=Message.template("请输入对应服务器ID:\n{list_msg}"))
async def _(state: T_State):
    logger.debug(f"server_id = {state['server_id']}")
    if str(state["server_id"]) == "0":
        await mcdel.finish("已取消")


@mcdel.handle()
async def _(state: T_State):
    server_name = state["server_list"][int(str(state["server_id"])) - 1]
    res = await MCServers.delete_server(server_name)
    if res:
        await mcdel.finish(f"已删除 {server_name}")
