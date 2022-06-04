import re
from random import randint

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
from nonebot.log import logger
from nonebot.params import CommandArg, State
from nonebot.typing import T_State
from nonebot_plugin_htmlrender import md_to_pic

from .mcping import ping
from .mcsm import *
from .yaml_loader import *

# from .config import Config

# plugin_config = Config.parse_obj(get_driver().config.dict())

__name__ = "mc"
mc_server = on_command("mc", priority=1)


def generate_server_list() -> dict:
    """返回服务器列表

    Args:
        res (list): 服务器列表响应

    Returns:
        dict: {"list_msg": list_msg, "server_list": server_id}
    """
    res = get_yaml_file()
    server_list_all: dict = res["server"]
    server_id = []
    for servers in server_list_all.keys():
        server_id.append(servers)
    # server_id = server_list_all.keys()
    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(server_id, start=1)])
    return {"list_msg": list_msg, "server_list": server_id}


def server_todo(todo: str) -> str:
    if todo in ("on", "start", "开服"):
        return "open"
    elif todo in ("off", "stop", "关服"):
        return "stop"
    elif todo in ("restart", "重启"):
        return "restart"
    return ""


@mc_server.handle()
async def mc_server_handle(arg: Message = CommandArg()):
    msg = ""
    ip = arg.extract_plain_text()
    if ip == "":
        data = get_yaml_file()["server"]
        for i in data.keys():
            # msg += f"{i}: {get_yaml_file()['server'][i]}\n"
            mc_status = ping(data[i]["ip"])
            # msg += "# " + i + "\n"
            msg += f"# {i} {data[i]['ip']}\n"
            for line in mc_status:
                msg += line + "\n"
            msg += "\n"
    await mc_server.finish(MessageSegment.image(await md_to_pic(msg)))


mcsm_ctl = on_command("mcsm")


@mcsm_ctl.handle()
async def mcsm_ctl_first_handle(
    event: MessageEvent,
    state: T_State = State(),
    arg: Message = CommandArg(),
):
    if str(event.user_id) not in get_yaml_file()["trust_id"]:
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
            res = generate_server_list()
            state["list_msg"] = res["list_msg"]
            state["server_list"] = res["server_list"]
            # await mcsm_ctl.send("请输入对应服务器ID:\n" + res["list_msg"])
    else:
        await mcsm_ctl.finish("使用 mcsm on|off|restart 开启|关闭|重启")


@mcsm_ctl.got("server_id", prompt=Message.template("请输入对应服务器ID:\n{list_msg}"))
async def mcsm_ctl_got_server_id(state: T_State = State()):
    logger.debug(f"server_id = {state['server_id']}")
    if str(state["server_id"]) == "0":
        await mcsm_ctl.finish("已取消")
    # await mcsm_ctl.send(f"请输入验证码: {state['code']}")


@mcsm_ctl.got("user_code", prompt=Message.template("请输入验证码: {code}"))
async def mcsm_ctl_got_user_code(state: T_State = State()):
    if str(state["user_code"]) != state["code"]:
        await mcsm_ctl.finish("已取消")


@mcsm_ctl.handle()
async def mcsm_ctl_finally(state: T_State = State()):
    try:
        if not state["server_name"]:
            server_name = state["server_list"][int(str(state["server_id"])) - 1]
        else:
            server_name = state["server_name"]

        await call_server(state["type"], **get_server_config(server_name))
        await mcsm_ctl.finish(f'已发送 {state["type"]} 指令')
    except HTTPStatusError as e:
        await mcsm_ctl.finish("HTTP错误: " + str(e))
    except MCSMAPIError as e:
        await mcsm_ctl.finish("MCSM API错误: " + str(e))
    except IndexError:
        await mcsm_ctl.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")
    except KeyError:
        await mcsm_ctl.finish("服务器不存在")
