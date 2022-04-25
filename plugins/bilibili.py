import json
import time

import aiohttp
from nonebot import on_message
from nonebot.log import logger
from bilibili_api import video
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, GroupMessageEvent
from nonebot.adapters.onebot.v11.exception import ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP

# from nonebot.typing import T_State

parse_bilibili_json = on_message(priority=1, permission=GROUP, block=False)


@parse_bilibili_json.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    try:
        data = json.loads(get_message_json(event.json())["data"])
    except KeyError:
        data = {}
    if data and data.get("prompt") == "[QQ小程序]哔哩哔哩":
        async with aiohttp.ClientSession() as session:
            async with session.get(
                data["meta"]["detail_1"]["qqdocurl"], timeout=7
            ) as response:
                url = str(response.url).split("?")[0]
                bvid = url.split("/")[-1]
                vd_info: dict = await video.Video(bvid=bvid).get_info()  # type: ignore
        # aid = vd_info["aid"]
        title = vd_info["title"]
        author = vd_info["owner"]["name"]
        reply = vd_info["stat"]["reply"]  # 回复
        favorite = vd_info["stat"]["favorite"]  # 收藏
        coin = vd_info["stat"]["coin"]  # 投币
        like = vd_info["stat"]["like"]  # 点赞
        # danmu = vd_info['stat']['danmaku']  # 弹幕
        date = time.strftime("%Y-%m-%d", time.localtime(vd_info["ctime"]))

        try:
            await parse_bilibili_json.send(
                MessageSegment.image(vd_info["pic"])
                + "\n"
                + MessageSegment.at(event.user_id)  # type: ignore
                + f"发送了一个傻卵QQ小程序：\n"
                f"标题：{title}\n"
                f"UP：{author}\n"
                f"上传日期：{date}\n"
                f"点赞：{like}，回复：{reply}，收藏：{favorite}，投币：{coin}\n"
                f"{url}"
            )
        except ActionFailed:
            pass
        try:
            await bot.delete_msg(message_id=event.message_id)
        except Exception as e:
            logger.opt(colors=True).warning("<blue>bilibili</blue> | {}".format(e))


def get_message_json(data: str) -> dict:
    data = json.loads(data)
    try:
        for msg in data["message"]:  # type: ignore
            if msg["type"] == "json":  # type: ignore
                return msg["data"]  # type: ignore
        return {}
    except Exception:
        return {}
