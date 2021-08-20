from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
import asyncio
from utils.utils import get_message_text, get_message_imgs
from nonebot.log import logger
from nonebot.adapters.cqhttp.message import MessageSegment
# from models.group_remind import GroupRemind
from utils.message_builder import image

__plugin_name__ = "广播 [Hidden]"

__plugin_usage__ = '广播- [消息] or [图片]'

broadcast = on_command("广播-", priority=1, permission=SUPERUSER, block=True)


@broadcast.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = get_message_text(event.json())
    imgs = get_message_imgs(event.json())
    rst = ''
    for img in imgs:
        rst += image(img)
    sid = bot.self_id
    gl = await bot.get_group_list(self_id=sid)
    gl = [g['group_id'] for g in gl]
    for g in gl:
        # if await GroupRemind.get_status(g, 'gb'):
        await asyncio.sleep(0.5)
        try:
            await bot.send_group_msg(self_id=sid, group_id=g, message=msg+rst)
            logger.info(f'群{g} 投递广播成功')
        except Exception as e:
            logger.error(f'群{g} 投递广播失败：{type(e)}')
            try:
                await broadcast.send(f'群{g} 投递广播失败：{type(e)}')
            except Exception as e:
                logger.critical(f'向广播发起者进行错误回报时发生错误：{type(e)}')
    await broadcast.send(f'广播完成！')
