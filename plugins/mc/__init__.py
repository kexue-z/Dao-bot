import re
from random import randint

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, ArgPlainText, Arg

# from nonebot.typing import T_State

from .mcping import mcping
from .mcsm import *
from .turstID import *

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
    if todo in ("on", "开服"):
        return "start_server"
    elif todo in ("off", "关服"):
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
    matcher: Matcher,
    arg: Message = CommandArg(),
):
    match = re.match(r"(on|开服|off|关服|restart|重启)\s?(.*)", arg.extract_plain_text())
    if match:
        matcher.set_arg("type", server_todo(match.group(1)))
        matcher.set_arg("code", str(randint(10, 99)))

        if match.group(2):
            matcher.set_arg("server_name", match.group(2))
            matcher.set_arg("server_id", "99")

            # await mcsm_ctl.send("请输入验证码: " + state["code"])
        else:
            matcher.set_arg("server_name", None)
            res = await server_get(apikey)
            res = generate_server_list(res)
            matcher.set_arg("server_list", res["server_list"])
            await mcsm_ctl.send("请输入对应服务器ID:\n" + res["list_msg"])
    logger.debug(
        f'type = {matcher.get_arg("type")}'
        f'code = {matcher.get_arg("code")}'
        f'server_name = {matcher.get_arg("server_name")}'
    )


@mcsm_ctl.got("server_id")
async def mcsm_ctl_got_server_id(
    matcher: Matcher,
    server_id: str = ArgPlainText("server_id"),
    # code: str = ArgPlainText("code"),
):
    logger.debug(f"server_id = {server_id}")
    if server_id == "0":
        await mcsm_ctl.finish("已取消")
    await mcsm_ctl.send(f"请输入验证码: {matcher.get_arg('code')}")


@mcsm_ctl.got("user_code")
async def mcsm_ctl_got_user_code(
    matcher: Matcher,
    user_code: str = ArgPlainText("user_code"),
):
    if user_code != matcher.get_arg("code"):
        await mcsm_ctl.finish("已取消")

    #     user_code = state["user_code"]
    #     logger.debug("user_code=" + user_code)
    #     if user_code != state["code"]:
    #         await mcsm_ctl.finish("已取消")

    # @mcsm_ctl.handle()
    # async def mcsm_ctl_finally(
    #     server_name: str = ArgPlainText("server_name"),
    #     type: str = ArgPlainText("type"),
    #     server_id: str = ArgPlainText("server_id"),
    #     server_list: list = Arg("server_list"),
    # ):
    server_name = matcher.get_arg("server_name")
    server_list = matcher.get_arg("server_list")
    server_id = matcher.get_arg("server_id").extract_plain_text()
    type = matcher.get_arg("type")

    if not server_name:
        server_name = server_list[int(server_id) - 1]
    else:
        server_name = server_name.extract_plain_text()

    res = await call_server(type, server_name, apikey)

    if res["status"] == 200:
        await mcsm_ctl.finish(f"已发送 {type} 指令")
    else:
        msg = f'错误: {res["error"]}'
        logger.error(msg)
        await mcsm_ctl.finish(msg)


#     if state["server_name"]:
#         res = await call_server(state["type"], state["server_name"], apikey)
#     else:
#         id = state["server_id"]
#         server_name = state["server_list"][int(id) - 1]
#         res = await call_server(state["type"], server_name, apikey)

#     if res["status"] == 200:
#         await mcsm_ctl.finish(f"已发送 {state['type']} 指令")
#     else:
#         await mcsm_ctl.finish(f"错误: {res['error']}")
