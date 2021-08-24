from nonebot import on_command
from nonebot.log import logger
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from nonebot.typing import T_State
import aiohttp


# __plugin_name__ = "语录"
# __plugin_usage__ = "用法： 二次元语录给你力量"


quotations = on_command("语录", aliases={"二次元", "二次元语录"}, priority=5, block=True)

url = "https://international.v1.hitokoto.cn/?c=a"


@quotations.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as response:
            data = await response.json()
    result = f'{data["hitokoto"]}\t——{data["from"]}'
    await quotations.send(result)
    logger.info(
        f"(USER {event.user_id}, GROUP {event.group_id if isinstance(event, GroupMessageEvent) else 'private'}) 发送语录:"
        + result
    )
