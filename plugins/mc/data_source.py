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
