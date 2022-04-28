from typing import List, Optional

from nonebot import get_bot, get_driver
from pydantic import BaseModel
from nonebot.log import logger
from nonebot.drivers.fastapi import Driver
from nonebot.adapters.onebot.v11 import Bot, Message

URL_BASE = "/notify"


class Notify(BaseModel):
    msg: str
    auth: str
    to_group: Optional[int] = None
    to_user: Optional[int] = None


auth: List[str] = get_driver().config.auth


def register_router_fastapi(driver: Driver):
    app = driver.server_app

    @app.post(URL_BASE)
    async def notify(notify: Notify):
        logger.debug(f"Notify: {notify.dict()}")
        if notify.auth not in auth:
            return {"message": "Not Authorized"}

        bot: Bot = get_bot()  # type: ignore

        if notify.to_group:
            return await bot.send_group_msg(
                group_id=notify.to_group,
                message=Message(notify.msg),
            )
        elif notify.to_user:
            return await bot.send_private_msg(
                user_id=notify.to_user,
                message=Message(notify.msg),
            )


def init():
    driver = get_driver()
    if driver.type == "fastapi":
        assert isinstance(driver, Driver)
        register_router_fastapi(driver)
    else:
        logger.warning(f"Driver {driver.type} not supported")
        return
    host = str(driver.config.host)
    port = driver.config.port
    if host in ["0.0.0.0", "127.0.0.1"]:
        host = "localhost"
    logger.opt(colors=True).info(
        f"Notify Api Runing at " f"<b><u>http://{host}:{port}{URL_BASE}</u></b>"
    )


init()
