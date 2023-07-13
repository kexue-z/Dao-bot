from models.mc import MCServers


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
    elif todo in ("off", "stop", "关服", "close"):
        return "stop"
    elif todo in ("restart", "重启"):
        return "restart"
    elif todo in ("kill", "终止", "强关"):
        return "kill"
    return ""


from re import findall
from typing import List

from mcstatus import JavaServer

from .data_models.mc_ping_res import MCPing
from .kook.data_source import get_server_status


async def mcping():
    servers = await get_server_status()

    mcpings: List[MCPing] = []

    for s in servers:
        js = await JavaServer.async_lookup(s.ip, timeout=5)
        status = js.status()

        motd = status.motd.to_plain()
        version_list = findall(r"\d+\.\d+(?:\.[\dxX]+)?", status.version.name)

        if len(version_list) != 1:
            version = f"{version_list[0]}-{version_list[-1]}"
        else:
            version = version_list[0]

        player_online = status.players.online
        max_online = status.players.max

        player_list = []
        if status.players.online:
            if status.players.sample:
                player_list = [
                    p.name
                    for p in status.players.sample
                    if p.id != "00000000-0000-0000-0000-000000000000"
                ]
        else:
            player_list = []

        latency = round(status.latency)

        mcpings.append(
            MCPing(
                name=s.name,
                ip=s.ip,
                version=version,
                player_online=player_online,
                max_online=max_online,
                player_list=player_list,
                latency=latency,
                motd=motd,
                mcsm_status=s.status,
            )
        )
    return mcpings


from .kook.utils import make_ping_card


async def mc_ping_kook():
    mcpings = await mcping()
    return make_ping_card(mcpings)


async def mc_ping_qq():
    mcpings = await mcping()
    STATUS_DICT = {
        -1: "状态未知",
        0: "已停止",
        1: "正在停止",
        2: "正在启动",
        3: "正在运行",
    }
    msg = ""
    for p in mcpings:
        msg += (
            f"# {p.name} {p.ip}\n"
            f"延迟: **{p.latency}ms**\n"
            f"MOTD: **{p.motd}**\n"
            f"游戏版本: **{p.version}**"
            f"玩家数: **{p.player_online}/{p.max_online}**"
            f"在线玩家: **{','.join([_p for _p in p.player_list])}**"
            f"MCSM 状态: **{STATUS_DICT[p.mcsm_status]}**"
        )

    return msg
