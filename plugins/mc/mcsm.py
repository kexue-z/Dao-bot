import nonebot
from nonebot import get_driver
from nonebot.log import logger
from httpx import Response, AsyncClient

from .config import Config

plugin_config = Config.parse_obj(get_driver().config.dict())
server = plugin_config.mcserver
apikey = plugin_config.mcserver_apikey


class MCSMAPIError(Exception):
    ...


class HTTPStatusError(Exception):
    ...


# 发送命令
# async def server_command(server_name: str, command: str, apikey: str = apikey):
#     async with AsyncClient() as client:
#         data = {"name": server_name, "command": command}
#         url = server + "execute/?apikey=" + apikey
#         res = await client.post(url, data=data)
#         return res.json()


# async def server_list(apikey: str = apikey) -> dict:
#     async with AsyncClient() as client:
#         url = server + "/server_list/?apikey=" + apikey
#         res = await client.get(url)
#         check(res)
#         return res.json()


async def call_server(
    type: str, instance_uuid: str, remote_uuid: str, apikey: str = apikey
) -> int:
    async with AsyncClient(follow_redirects=True) as client:
        params = {
            "apikey": apikey,
            "remote_uuid": remote_uuid,
            "uuid": instance_uuid,
        }
        res = await client.get(f"{server}/api/protected_instance/{type}", params=params)
    return check(res)


def check(res: Response) -> int:
    logger.debug(res.status_code)
    logger.debug(res.content)
    logger.debug(res.url)
    if res.status_code != 200:
        raise HTTPStatusError("Error: " + str(res.status_code))

    if res.json()["status"] != 200:
        raise MCSMAPIError(res.json()["error"])

    return int(res.json()["status"])
