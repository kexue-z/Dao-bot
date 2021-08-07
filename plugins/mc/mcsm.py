import asyncio
from httpx import AsyncClient
import nonebot

server = nonebot.get_driver().config.mcserver
apikey = nonebot.get_driver().config.mcserver_apikey

# 开启服务器
async def server_on(server_name: str, apikey: str):
    async with AsyncClient() as client:
        url = server + 'start_server/' + server_name + '?apikey=' + apikey
        res = await client.get(url)
        return res.json()
    
# 关闭服务器
async def server_off(server_name: str, apikey: str):
    async with AsyncClient() as client:
        url = server + 'stop_server/' + server_name + '?apikey=' + apikey
        res = await client.get(url)
        return res.json()
    
# 重启服务器
async def server_restart(server_name: str, apikey: str):
    async with AsyncClient() as client:
        url = server + 'restart_server/' + server_name + '?apikey=' + apikey
        res = await client.get(url)
        return res.json()
    
# 发送命令
async def server_command(server_name: str, apikey: str, command: str):
    async with AsyncClient() as client:
        data = {'name': server_name, 'command': command}
        url = server + 'execute/?apikey=' + apikey
        res = await client.post(url,data=data)
        return res.json()
    

async def server_get(apikey: str):
    async with AsyncClient() as client:
        url = server + 'server_list/?apikey=' + apikey
        res = await client.get(url)
        return res.json()
    
if __name__ == '__main__':
    res = asyncio.run(
        server_command('13server',apikey,'list')
        )
    print(res)