from httpx import AsyncClient
from nonebot import get_driver

docker_url = get_driver().config.docker_url


async def pz_server(way: str):
    async with AsyncClient() as client:
        url = docker_url + "containers/" + "pzserver" + "/" + way
        res = await client.post(url,timeout=120)
        return res


