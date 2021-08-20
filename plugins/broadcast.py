from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.permission import SUPERUSER
import asyncio
from utils.utils import get_message_text, get_message_imgs
from nonebot.log import logger
from nonebot.adapters.cqhttp.message import MessageSegment
# from models.group_remind import GroupRemind
# from utils.message_builder import image

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



def image(
    img_name: str = None, path: str = None, abspath: str = None, b64: str = None
) -> MessageSegment or str:
    """
    说明：
        生成一个 MessageSegment.image 消息
        生成顺序：绝对路径(abspath) > base64(b64) > img_name
    参数：
        :param img_name: 图片文件名称，默认在 resource/img 目录下
        :param path: 图片所在路径，默认在 resource/img 目录下
        :param abspath: 图片绝对路径
        :param b64: 图片base64
    """
    if abspath:
        return (
            MessageSegment.image("file:///" + abspath)
            if os.path.exists(abspath)
            else ""
        )
    elif b64:
        return MessageSegment.image(b64 if "base64://" in b64 else "base64://" + b64)
    else:
        if "http" in img_name:
            return MessageSegment.image(img_name)
        if len(img_name.split(".")) == 1:
            img_name += ".jpg"
        file = (
            Path(IMAGE_PATH) / path / img_name if path else Path(IMAGE_PATH) / img_name
        )
        if file.exists():
            return MessageSegment.image(f"file:///{file.absolute()}")
        else:
            logger.warning(f"图片 {file.absolute()}缺失...")
            return ""




