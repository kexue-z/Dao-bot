import re
from random import randint

from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.params import CommandArg
from nonebot import require, on_command
from nonebot.adapters.onebot.v11 import (
    Message,
    MessageEvent,
    MessageSegment,
    Bot,
    Event,
)
from nonebot.permission import SUPERUSER, SuperUser

from .models import MCTrustIDs, MCServers
from .mcsm import *
from .mcping import ping


require("nonebot_plugin_tortoise_orm")
require("nonebot_plugin_htmlrender")
from nonebot_plugin_tortoise_orm import add_model  # noqa: E402
from nonebot_plugin_htmlrender import md_to_pic  # noqa: E402

add_model("plugins.mc.models")

# from .config import Config

# plugin_config = Config.parse_obj(get_driver().config.dict())

__name__ = "mc"


async def generate_server_list() -> dict:
    """返回服务器列表

    Args:
        res (list): 服务器列表响应

    Returns:
        dict: {"list_msg": list_msg, "server_list": server_id}
    """
    # res = get_yaml_file()
    # server_list_all: dict = res["server"]
    servers = await MCServers.get_all_servers_ip()
    # server_id = []
    # for servers in server_list_all.keys():
    #     server_id.append(servers)
    # server_id = server_list_all.keys()
    server_id = [server[0] for server in servers]
    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(server_id, start=1)])
    return {"list_msg": list_msg, "server_list": server_id}


def server_todo(todo: str) -> str:
    if todo in ("on", "start", "开服", "open"):
        return "open"
    elif todo in ("off", "stop", "关服", "stop"):
        return "stop"
    elif todo in ("restart", "重启"):
        return "restart"
    elif todo in ("kill", "终止", "强关"):
        return "kill"
    return ""


mc_server = on_command("mc", priority=1)


@mc_server.handle()
async def mc_server_handle(arg: Message = CommandArg()):
    msg = ""
    ip = arg.extract_plain_text()
    if ip == "":
        # data = get_yaml_file()["server"]
        # for i in data.keys():
        # msg += f"{i}: {get_yaml_file()['server'][i]}\n"
        # servers = await
        servers = await MCServers.get_all_servers_ip()
        for server in servers:

            mc_status = ping(server[1])
            # msg += "# " + i + "\n"
            msg += f"# {server[0]} {server[1]}\n"
            for line in mc_status:
                msg += line + "\n"
            msg += "\n"
    await mc_server.finish(MessageSegment.image(await md_to_pic(msg)))


mcadd = on_command("mcadd", permission=SUPERUSER)


@mcadd.handle()
async def _(state: T_State, arg: Message = CommandArg()):
    state["name"], name = arg.extract_plain_text()
    if name.strip() == "":
        await mcadd.finish("????")
    if await MCServers.exists(name=name):
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


def check_superuser(bot: Bot, event: Event):
    try:
        user_id = event.get_user_id()
    except Exception:
        return False
    return (
        f"{bot.adapter.get_name().split(maxsplit=1)[0].lower()}:{user_id}"
        in bot.config.superusers
        or user_id in bot.config.superusers  # 兼容旧配置
    )


mcsm_add = on_command("mcsmadd")


@mcsm_add.handle()
async def _(bot: Bot, event: MessageEvent, arg: Message = CommandArg()):
    user_id = 0
    if not (
        event.user_id in await MCTrustIDs.get_all_enabled_ids()
        or check_superuser(bot, event)
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
                Message.template("已添加 {}".format(MessageSegment.at(user_id)))
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
        r"(on|start|开服|off|stop|关服|restart|重启)\s?(.*)", arg.extract_plain_text()
    )
    if match:
        state["type"] = server_todo(match.group(1))
        state["code"] = str(randint(10, 99))

        if match.group(2):
            state["server_name"] = match.group(2)
            state["server_id"] = "99"
            logger.debug(f"{state['server_name']}")

            # await mcsm_ctl.send("请输入验证码: " + state["code"])
        else:
            state["server_name"] = None
            res = await generate_server_list()
            state["list_msg"] = res["list_msg"]
            state["server_list"] = res["server_list"]
            # await mcsm_ctl.send("请输入对应服务器ID:\n" + res["list_msg"])
    else:
        await mcsm_ctl.finish("使用 mcsm on|off|restart 开启|关闭|重启")


@mcsm_ctl.got("server_id", prompt=Message.template("请输入对应服务器ID:\n{list_msg}"))
async def mcsm_ctl_got_server_id(state: T_State):
    logger.debug(f"server_id = {state['server_id']}")
    if str(state["server_id"]) == "0":
        await mcsm_ctl.finish("已取消")
    # await mcsm_ctl.send(f"请输入验证码: {state['code']}")


@mcsm_ctl.got("user_code", prompt=Message.template("请输入验证码: {code}"))
async def mcsm_ctl_got_user_code(state: T_State):
    if str(state["user_code"]) != state["code"]:
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.handle()
async def mcsm_ctl_finally(state: T_State):
    try:
        if not state["server_name"]:
            server_name = state["server_list"][int(str(state["server_id"])) - 1]
        else:
            server_name = state["server_name"]
        res = await MCServers.get_server_data(server_name)
        await call_server(state["type"], **res)
        await mcsm_ctl.finish(f'已发送 {state["type"]} 指令')
    except HTTPStatusError as e:
        await mcsm_ctl.finish("HTTP错误: " + str(e))
    except MCSMAPIError as e:
        await mcsm_ctl.finish("MCSM API错误: " + str(e))
    except IndexError:
        await mcsm_ctl.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")
    except KeyError:
        await mcsm_ctl.finish("服务器不存在")
