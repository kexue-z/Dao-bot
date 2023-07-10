import re
import codecs
from typing import List
from json.decoder import JSONDecodeError

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


async def call_command(
    command: str, instance_uuid: str, remote_uuid: str, apikey: str = apikey
) -> int:
    async with AsyncClient(follow_redirects=True) as client:
        params = {
            "command": command,
            "apikey": apikey,
            "remote_uuid": remote_uuid,
            "uuid": instance_uuid,
        }
        res = await client.get(
            f"{server}/api/protected_instance/command", params=params
        )
    return check(res)


async def get_output(instance_uuid: str, remote_uuid: str, apikey: str = apikey):
    async with AsyncClient(follow_redirects=True) as client:
        params = {
            "apikey": apikey,
            "remote_uuid": remote_uuid,
            "uuid": instance_uuid,
        }
        res = await client.get(
            f"{server}/api/protected_instance/outputlog", params=params
        )
    check(res)
    data: str = res.json()["data"]
    data = data[len(data) // 512 :]
    return normalize_text(data)


def normalize_text(text):
    """Removes escape sequences, color codes and prompts.
    Replaces Windows-style line endings with Unix-style."""

    # Remove escape characters
    text = codecs.decode(text, "unicode_escape")

    # Remove color codes
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    text = ansi_escape.sub("", text)

    # Remove prompts
    lines = text.split("\n")
    lines = [line.lstrip(">") for line in lines]
    text = "\n".join(lines)
    text = text.replace("\n ", "")

    # Replace Windows-style line endings with Unix-style
    text = text.replace("\r\n", "\n")

    return text


def check(res: Response) -> int:
    logger.debug(res.status_code)
    logger.debug(res.text)
    logger.debug(res.url)

    try:
        if res.json()["status"] != 200:
            raise MCSMAPIError(res.json()["data"])

        return int(res.json()["status"])
    except JSONDecodeError:
        raise HTTPStatusError("服务器连接失败？")


async def search_remote_services(
    remote_uuid: str, page: int = 1, page_size=10, apikey: str = apikey
) -> List:
    async with AsyncClient(follow_redirects=True) as client:
        params = {
            "apikey": apikey,
            "remote_uuid": remote_uuid,
            "page_size": page_size,
            "page": page,
        }
        res = await client.get(
            f"{server}/api/service/remote_service_instances", params=params
        )
    try:
        if res.json()["status"] != 200:
            raise MCSMAPIError(res.json()["data"])

        return res.json()["data"]

    except JSONDecodeError:
        raise HTTPStatusError("服务器连接失败？")
