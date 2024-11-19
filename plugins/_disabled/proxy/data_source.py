import json

from httpx import AsyncClient


async def get_Proxies(url: str) -> list:
    async with AsyncClient() as client:
        res = await client.get(url + "proxies")
        res = res.json()
        return res["proxies"]["Proxy"]["all"]


async def get_Proxies_delay(
    proxies: list,
    url: str,
    timeout: int = 3000,
    testing_url: str = "http://www.gstatic.com/generate_204",
) -> list:
    delay_list = []
    params = {"timeout": timeout, "url": testing_url}
    for proxy in proxies:
        async with AsyncClient() as client:
            res = await client.get(url + "proxies/" + proxy + "/delay", params=params)
            delay_list.append(str(res.json().get("delay", "TimeOut")))
    return delay_list


async def Select_Proxy(name: str, url: str) -> int:
    async with AsyncClient() as client:
        data = {"name": name}
        res = await client.put(url + "proxies/Proxy", data=json.dumps(data))
        return res.status_code
