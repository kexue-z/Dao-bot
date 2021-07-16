from requests import get
import json

from nonebot import on_command
from nonebot.typing import T_State
# from nonebot.plugin import require
from nonebot.adapters.cqhttp import (
    Bot,
    MessageEvent,
    PrivateMessageEvent,
    GroupMessageEvent
)

url = "https://192.168.0.199:23333/api/status/"
data_dir = "./data/mcserver/"
status = {}
server_data = {}

# scheduler = require("nonebot_plugin_apscheduler").scheduler

def get_status(server_name) -> json:
    """网页读取json"""
    response = get(url+server_name,verify=False)
    return json.loads(response.text)

def load_data(id) -> list:
    """读取订阅数据"""
    try:
        # 打开已存在文件
        with open(data_dir+"sub_data.json",mode="r") as server:
            server_data = json.load(server)
            if id in server_data:
                return server_data[id]
            else:
                return None
    except FileNotFoundError:
        # 不存在则创建文件夹和文件
        try:
            import os
            os.makedirs(data_dir)
        except FileExistsError:
            pass
        with open(data_dir+"sub_data.json",mode="w") as server:
            json.dump({},server)
    
def save_server(status):
    """保存服务器信息数据用"""
    try:
        # 打开已存在文件
        with open(data_dir+"server_data.json",mode="r") as server:
            server_data = json.load(server)
        server_data.update(status)
    except FileNotFoundError:
        # 无文件
        server_data = {}
    
    # 保存
    with open(data_dir+"server_data.json",mode="w+") as server:
        json.dump(status,server,sort_keys=True,indent=4)
            
def add_server(id, name):
    """群添加服务器"""
    with open(data_dir+"sub_data.json",mode="r") as server:
        server_data = dict(json.load(server))
        try:
            if (id in server_data
                    and name not in server_data[id]):
                server_data[id].append(name)
            else:
                server_data[id] = [name]
        except:
            server_data = {}
            server_data[id] = [name]

    with open(data_dir+"sub_data.json",mode="w") as server:
        json.dump(server_data,server,sort_keys=True,indent=4)

def remove_server(id, name):
    """移除服务器"""
    with open(data_dir+"sub_data.json",mode="r") as server:
        server_data = json.load(server)
        print(server_data)
    print(server_data)

    if (id in server_data) and (name in server_data[id]):
        server_data[id].remove(name)
        print(server_data)
    with open(data_dir+"sub_data.json",mode="w") as server:
        json.dump(server_data,server,sort_keys=True,indent=4)

# mc指令 列出服务器
mc_server = on_command('mc', priority=1)

@mc_server.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    id = event.user_id if isinstance(event, PrivateMessageEvent) else event.group_id 
    servers = load_data(str(id))
    if servers:
        msg = ""
        for server in servers:
            status.update({server: get_status(server)})
            msg += f"{server:=^20}\n"
            try:
                if status[server]["status"]:
                    msg += f"服务器状态: 在线\n"
                    msg += f"在线人数: {status[server]['current_players']}\n"
                    msg += f"最大人数: {status[server]['max_players']}\n"
                    msg += f"游戏版本: {status[server]['version']}\n"
                else:
                    msg += f"服务器状态: 离线\n"
                    msg += f"最后在线: {status[server]['lastDate']}\n"
            except:
                pass
        save_server(status)
    else:
        msg = "还没添加服务器"

    await bot.send(event,msg)

# mcadd指令 添加服务器
mcadd = on_command('mcadd', priority=2)

@mcadd.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):

    id = event.user_id if isinstance(event, PrivateMessageEvent) else event.group_id 
    add_server(str(id),str(event.get_message()))
    message = f"已添加服务器:{str(event.get_message())}"
    await bot.send(event,message)

# mcremove指令 删除服务器
mcremove = on_command('mcremove', priority=2)

@mcremove.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    id = event.user_id if isinstance(event, PrivateMessageEvent) else event.group_id 
    remove_server(str(id),str(event.get_message()))
    message = (f"已移除服务器:{str(event.get_message())}"    )
    await bot.send(event,message)

