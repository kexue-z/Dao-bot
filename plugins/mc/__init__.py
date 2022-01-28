import re
from random import randint

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.log import logger
from nonebot.params import CommandArg, ArgPlainText, State
from nonebot.typing import T_State
from nonebot.exception import ActionFailed
from .mcping import mcping
from .mcsm import *
from .turstID import *


__name__ = "mc"
mc_server = on_command("mc", priority=1)


def generate_server_list(res: list) -> dict:
    """返回服务器列表

    Args:
        res (list): 服务器列表响应

    Returns:
        dict: {"list_msg": list_msg, "server_list": server_id}
    """
    server_list_all = res["data"]
    server_id = []
    for servers in server_list_all:
        server_id.append(str(f"{servers['data']['name']}"))
    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(server_id, start=1)])
    return {"list_msg": list_msg, "server_list": server_id}


def server_todo(todo: str) -> str:
    if todo in ("on", "start", "开服"):
        return "start_server"
    elif todo in ("off", "stop", "关服"):
        return "stop_server"
    elif todo in ("restart", "重启"):
        return "restart_server"


@mc_server.handle()
async def mc_server_handle(arg: Message = CommandArg()):
    msg = ""
    ip = arg.extract_plain_text()
    mc_status = mcping(ip)
    for line in mc_status:
        msg += line
    await mc_server.finish(msg)


mcsm_ctl = on_command("mcsm")


@mcsm_ctl.handle()
async def mcsm_ctl_first_handle(
    state: T_State = State(),
    arg: Message = CommandArg(),
):
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
            res = await server_list(apikey)
            res = generate_server_list(res)
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

        await call_server(state["type"], server_name)
        await mcsm_ctl.finish(f'已发送 {state["type"]} 指令')
    except HTTPStatusError as e:
        await mcsm_ctl.finish("HTTP错误: " + str(e))
    except MCSMAPIError as e:
        await mcsm_ctl.finish("MCSM API错误: " + str(e))
    except IndexError as e:
        await mcsm_ctl.finish(f"这个列表就那么一点，你输个了啥？{state['server_id']}？？？")

