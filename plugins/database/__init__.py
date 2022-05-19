from nonebot import get_driver
from databases import Database
from nonebot.log import logger

from .config import Config

db_config = Config.parse_obj(get_driver().config.dict())
driver = get_driver()

db = Database(
    f"postgresql://{db_config.db_user}:{db_config.db_name}@{db_config.db_host}:{db_config.db_port}/{db_config.db_name}"
)


@driver.on_startup
async def connect():
    await db.connect()
    logger.opt(colors=True).success("<y>连接到 Postgresql 数据库</y>")


@driver.on_shutdown
async def disconnect():
    await db.disconnect()
    logger.opt(colors=True).success("<y>中断连接 Postgresql 数据库</y>")
