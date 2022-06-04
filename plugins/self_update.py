from httpx import AsyncClient
from nonebot import get_driver, on_command
from nonebot.log import logger
from nonebot.permission import SUPERUSER
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    github_api_key: str


API_KEY = Config.parse_obj(get_driver().config.dict()).github_api_key
API_URL = "https://api.github.com/repos/kexue-z/Dao-bot/actions/workflows/auto-update.yml/dispatches"


auto_update = on_command("自我更新", permission=SUPERUSER, block=True, priority=1)


@auto_update.handle()
async def _():
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {API_KEY}",
    }
    data = {"ref": "master"}
    async with AsyncClient() as client:
        res = await client.post(API_URL, headers=headers, json=data)
        if res.status_code == 204:
            logger.success("已发起自我更新请求")
        await auto_update.finish("已发起自我更新请求")
