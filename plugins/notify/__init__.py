from typing import Optional

from nonebot import get_bot, get_driver
from nonebot.log import logger
from nonebot.drivers.fastapi import Driver
from nonebot.adapters.onebot.v11 import Bot, Message

URL_BASE = "/notify"


def register_router_fastapi(driver: Driver):
    app = driver.server_app

    @app.get(URL_BASE)
    async def notify(
        msg: str,
        to_group: Optional[int] = None,
        to_user: Optional[int] = None,
    ):
        bot: Bot = get_bot()  # type: ignore

        if to_group:
            return await bot.send_group_msg(
                group_id=to_group,
                message=Message(msg),
            )
        elif to_user:
            return await bot.send_private_msg(
                user_id=to_user,
                message=Message(msg),
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
