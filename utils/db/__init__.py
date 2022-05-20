from nonebot import get_driver
from tortoise import Tortoise
from nonebot.log import logger

from .config import Config

db_config = Config.parse_obj(get_driver().config.dict())
driver = get_driver()


@driver.on_startup
async def connect():
    await Tortoise.init(
        db_url=f"postgres://{db_config.db_user}@{db_config.db_host}:{db_config.db_port}/{db_config.db_name}",
        modules={"models": ["utils.db.models"]},
    )
    await Tortoise.generate_schemas()
    logger.opt(colors=True).success("<y>连接到 Postgresql 数据库</y>")


@driver.on_shutdown
async def disconnect():
    await Tortoise.close_connections()
    logger.opt(colors=True).success("<y>中断连接 Postgresql 数据库</y>")
