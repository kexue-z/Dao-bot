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
    logger.debug(res.text)
    logger.debug(res.url)
    from json.decoder import JSONDecodeError

    try:
        if res.json()["status"] != 200:
            raise MCSMAPIError(res.json()["data"])

        return int(res.json()["status"])
    except JSONDecodeError:
        raise HTTPStatusError("服务器连接失败？")
