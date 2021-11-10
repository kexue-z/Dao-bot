from .mcping import mcping
from .mcsm import *

from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, Message
from nonebot.rule import to_me
from random import randint
from nonebot.permission import SUPERUSER, USER, MESSAGE
from nonebot.log import logger

from .turstID import *

mc_server = on_command("mc", priority=1)


@mc_server.handle()
async def mc_server(bot: Bot, event: MessageEvent, state: T_State):
    msg = ""
    ip = str(event.get_message())
    mc_status = mcping(ip)
    for line in mc_status:
        msg += line
    await bot.send(event, msg)


mc_server_on = on_command("mcon", aliases={"开服", "开启服务器"}, priority=1)


@mc_server_on.handle()
async def mc_server_on_frist(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.user_id) not in get_yaml_file():
        await mc_server_on.finish("你没有权限")
    res = await server_get(apikey)
    server_list_all = res["data"]
    serverID = []
    for servers in server_list_all:
        serverID.append(str(f"{servers['data']['name']}"))

    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(serverID, start=1)])

    server_name = str(event.message)
    if server_name:
        state["server_name"] = server_name
    code = str(randint(10, 99))
    await bot.send(event, f"请输入对应服务器ID:\n{list_msg}")
    state["serverlist"] = serverID
    state["code"] = code


@mc_server_on.got("server_id")
async def mc_server_on_get_server_name(bot: Bot, event: MessageEvent, state: T_State):
    code = state["code"]
    await bot.send(event, message=f"请输入验证码: {code}")


@mc_server_on.got("user_code")
async def mc_server_on_got_code(bot: Bot, event: MessageEvent, state: dict):
    if state["user_code"] == "0":
        await mc_server_on.finish()


@mc_server_on.handle()
async def mc_server_on_done(bot: Bot, event: MessageEvent, state: T_State):
    id = state["server_id"]
    server_name = state["serverlist"][int(id) - 1]
    code = state["code"]
    user_Code = state["user_code"]
    logger.opt(colors=True).info(
        f"<red>MCSM开服</red> | 获取ID: {id}, 服务器ID: {server_name}, 验证码: {code}, 用户验证码: {user_Code} "
    )
    if user_Code == code:
        res = await server_on(server_name, apikey)
        logger.opt(colors=True).info(f"<red>MCSM开服</red> | 已开服: {res}")
        if res["status"] == 200:
            await bot.send(event, message=f"已发送启动指令")
        else:
            await bot.send(event, message=f'错误: {res["error"]}')


mc_server_off = on_command("mcoff", aliases={"关服", "关闭服务器"}, priority=1)


@mc_server_off.handle()
async def mc_server_on_frist(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.user_id) not in get_yaml_file():
        await mc_server_on.finish("你没有权限")
    res = await server_get(apikey)
    server_list_all = res["data"]
    serverID = []
    for servers in server_list_all:
        serverID.append(str(f"{servers['data']['name']}"))

    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(serverID, start=1)])

    server_name = str(event.message)
    if server_name:
        state["server_name"] = server_name
    code = str(randint(10, 99))
    await bot.send(event, f"请输入对应服务器ID:\n{list_msg}")
    state["serverlist"] = serverID
    state["code"] = code


@mc_server_off.got("server_id")
async def mc_server_off_get_server_name(bot: Bot, event: MessageEvent, state: T_State):
    code = state["code"]
    await bot.send(event, message=f"请输入验证码: {code}")


@mc_server_off.got("user_code")
async def mc_server_off_got_code(bot: Bot, event: MessageEvent, state: dict):
    if state["user_code"] == "0":
        await mc_server_on.finish()


@mc_server_off.handle()
async def mc_server_off_done(bot: Bot, event: MessageEvent, state: T_State):
    id = state["server_id"]
    server_name = state["serverlist"][int(id) - 1]
    code = state["code"]
    user_Code = state["user_code"]
    logger.opt(colors=True).info(
        f"<red>MCSM开服</red> | 获取ID: {id}, 服务器ID: {server_name}, 验证码: {code}, 用户验证码: {user_Code} "
    )
    if user_Code == code:
        res = await server_off(server_name, apikey)
        logger.opt(colors=True).info(f"<red>MCSM关服</red> | 已关服: {res}")
        if res["status"] == 200:
            await bot.send(event, message=f"已发送关闭指令")
        else:
            await bot.send(event, message=f'错误: {res["error"]}')


mc_server_restart = on_command("mcrestart", aliases={"重启服", "重启服务器"}, priority=1)


@mc_server_restart.handle()
async def mc_server_restart_frist(bot: Bot, event: MessageEvent, state: T_State):
    if str(event.user_id) not in get_yaml_file():
        await mc_server_on.finish("你没有权限")
    res = await server_get(apikey)
    server_list_all = res["data"]
    serverID = []
    for servers in server_list_all:
        serverID.append(str(f"{servers['data']['name']}"))

    list_msg = "\n".join([f"{i}: {line}" for i, line in enumerate(serverID, start=1)])

    server_name = str(event.message)
    if server_name:
        state["server_name"] = server_name
    code = str(randint(10, 99))
    await bot.send(event, f"请输入对应服务器ID:\n{list_msg}")
    state["serverlist"] = serverID
    state["code"] = code


@mc_server_restart.got("server_id")
async def mc_server_restart_get_server_name(
    bot: Bot, event: MessageEvent, state: T_State
):
    code = state["code"]
    await bot.send(event, message=f"请输入验证码: {code}")


@mc_server_restart.got("user_code")
async def mc_server_restart_got_code(bot: Bot, event: MessageEvent, state: dict):
    if state["user_code"] == "0":
        await mc_server_on.finish()


@mc_server_restart.handle()
async def mc_server_restart_done(bot: Bot, event: MessageEvent, state: T_State):
    id = state["server_id"]
    server_name = state["serverlist"][int(id) - 1]
    code = state["code"]
    user_Code = state["user_code"]
    if user_Code == code:
        res = await server_restart(server_name, apikey)
        logger.opt(colors=True).info(f"<red>MCSM重启</red> | 已重启: {res}")
        if res["status"] == 200:
            await bot.send(event, message=f"已发送重启指令")
        else:
            await bot.send(event, message=f'错误: {res["error"]}')
