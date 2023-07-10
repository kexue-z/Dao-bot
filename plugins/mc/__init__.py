from nonebot import require

require("nonebot_plugin_tortoise_orm")
require("nonebot_plugin_htmlrender")

from nonebot_plugin_htmlrender import md_to_pic
from nonebot_plugin_tortoise_orm import add_model

add_model("plugins.mc.models")


import re
from random import randint

from dateutil import tz
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER
from nonebot.internal.adapter.bot import Bot
from nonebot import on_notice, get_driver, on_command
from nonebot.adapters.kaiheila import Event as KEvent
from nonebot.adapters.kaiheila import Event as KHLEvent
from nonebot.adapters.kaiheila import Message as KMessage
from nonebot_plugin_saa import Text, Image, MessageFactory
from nonebot.adapters.kaiheila import MessageSegment as KMS
from nonebot.adapters.onebot.v11 import (
    Event,
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent,
)

from .mcsm import *
from .mcping import ping
from .kook.data_source import get_server_status
from .data_source import server_todo, generate_server_list
from .models import MCServers, MCTrustIDs, ServerCommandHistory

mc_server = on_command("mc", priority=1)


@mc_server.handle()
async def mc_server_handle(bot: Bot, event: MessageEvent | KHLEvent):
    msg = ""

    servers = await MCServers.get_all_servers_ip()
    for server in servers:
        mc_status = ping(server[1])
        # msg += "# " + i + "\n"
        msg += f"# {server[0]} {server[1]}\n"
        for line in mc_status:
            msg += line + "\n"
        msg += "\n"

    msg = MessageFactory(Image(await md_to_pic(msg)))
    await msg.send()
    await mc_server.finish()
    # await mc_server.finish(MessageSegment.image(await md_to_pic(msg)))


mcadd = on_command("mcadd", permission=SUPERUSER)


@mcadd.handle()
async def _(state: T_State, args: Message = CommandArg()):
    name = args.extract_plain_text()
    if name.strip() != "":
        state["name"] = name


@mcadd.got("name", prompt="请输入名称")
async def _(state: T_State, args: Message = CommandArg()):
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


mcdel = on_command("mcdel", permission=SUPERUSER)


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


def check_superuser(event: Event):
    config = get_driver().config.superusers

    if event.get_user_id() in config:
        return True
    else:
        return False


mcsm_add = on_command("mcsmadd")


@mcsm_add.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    user_id = 0
    if not (
        event.user_id in await MCTrustIDs.get_all_enabled_ids()
        or check_superuser(event)
    ):
        await mcsm_add.finish("你没有权限使用这个命令")
    for a in arg:
        if a.type == "at":
            user_id: int = int(a.data["qq"])
            break

    if user_id:
        if not await MCTrustIDs.exists(user_id=user_id):
            await MCTrustIDs.add_id(user_id=user_id)
            await mcsm_add.finish(
                Message.template("已添加 {}").format(MessageSegment.at(user_id))
            )

    await mcsm_add.finish(Message("添加失败, 或已经存在"))


mcsm_ctl = on_command("mcsm")


@mcsm_ctl.handle()
async def mcsm_ctl_first_handle(
    event: MessageEvent,
    state: T_State,
    arg: Message = CommandArg(),
):
    if event.user_id not in await MCTrustIDs.get_all_enabled_ids():
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
async def mcsm_ctl_got_server_id(state: T_State):
    logger.debug(f"server_id = {state['server_id']}")
    if str(state["server_id"]) == "0":
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.got("user_code", prompt=Message.template("请输入验证码: {code}"))
async def mcsm_ctl_got_user_code(state: T_State):
    if str(state["user_code"]) != state["code"]:
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.handle()
async def mcsm_ctl_finally(state: T_State, event: Event):
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


mcsm_command = on_command("mcc")


@mcsm_command.handle()
async def _(
    event: MessageEvent,
    state: T_State,
    args: Message = CommandArg(),
):
    if event.user_id not in await MCTrustIDs.get_all_enabled_ids():
        await mcsm_command.finish("你没有权限使用这个命令")
    for i in args:
        if i.type != "text":
            await mcsm_command.finish("指令中不能包含除文本以外的内容哦~")

    command = args.extract_plain_text()
    if command.strip() != "":
        state["command"] = command

    if command.startswith("/"):
        await mcsm_command.finish("不需要 / , 重新执行指令")

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
async def _(state: T_State, event: MessageEvent):
    logger.debug(state)
    try:
        server_name = state["server_list"][int(str(state["server_id"])) - 1]

        server_data = await MCServers.get_server_data(server_name)

        await call_command(command=state["command"], **server_data)

        await ServerCommandHistory.add_command_record(
            command=state["command"],
            user_id=event.user_id,
            target_instance_uuid=server_data["instance_uuid"],
            target_remote_uuid=server_data["remote_uuid"],
            is_success=True,
        )

        # output = await get_output(**server_data)
        # logger.debug(output)

        # await mcsm_command.finish(
        #     MessageSegment.image(
        #         await md_to_pic(TEXT_TEMPLATE.format(output=output), width=1200)
        #     )
        # )

        await mcsm_command.finish("执行成功")

    except HTTPStatusError as e:
        await mcsm_command.finish("HTTP错误: " + str(e))

    except MCSMAPIError as e:
        await mcsm_command.finish("MCSM API错误: " + str(e))

    except IndexError:
        await mcsm_command.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")

    except KeyError:
        await mcsm_command.finish("服务器不存在")


mcsm_command_history = on_command("命令历史")


@mcsm_command_history.handle()
async def _(
    bot: Bot, event: GroupMessageEvent | MessageEvent, args: Message = CommandArg()
):
    user_id = None

    if isinstance(event, GroupMessageEvent):
        for a in args:
            if a.type == "at":
                user_id = int(a.data["qq"])
                break

    res = await ServerCommandHistory.get_recent_history(user_id=user_id)

    text = "# 命令执行历史\n\n"

    for i in res:
        user_info = await bot.get_stranger_info(user_id=i.user_id)
        nickname = "{}({})".format(user_info["nickname"], user_info["user_id"])
        # nickname = "123"
        server_name = await MCServers.get_server_name_by_uuid(i.target_instance_uuid)
        text += (
            f"- {nickname}\n"
            f"\t - 目标服务器: `{server_name}`\n"
            f"\t - 指令: `{i.command.strip()}`\n"
            f"\t - 时间: `{i.time.astimezone(tz.tzlocal()).strftime('%m/%d, %H:%M:%S')}`\n"
        )

    await mcsm_command_history.finish(MessageSegment.image(await md_to_pic(text)))


kmcsm = on_command("mcsm", priority=1, block=True)


@kmcsm.handle()
async def _(event: KEvent):
    logger.debug("KOOK!")
    card = await get_server_status()
    await kmcsm.finish(KMessage(KMS.Card(card)))


kmcsm_button = on_notice()


async def _(event: KEvent):
    logger.debug(event)
