import base64
from re import findall

import httpx
import nonebot
from httpx import AsyncClient
from nonebot import logger

from .save_img import *


async def ghs_pic3(keyword="", r18=False) -> str:
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/v2"
        params = {"keyword": keyword, "r18": 1 if r18 else 0, "size": "regular"}
        try:
            res = await client.get(req_url, params=params, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return "Error:", f"API异常{e}", False
        try:
            setu_title = res.json()["data"][0]["title"]
            setu_url = res.json()["data"][0]["urls"]["regular"]
            base64 = await downPic(setu_url, r18)
            setu_pid = res.json()["data"][0]["pid"]
            setu_author = res.json()["data"][0]["author"]
            if type(base64) == str:
                pic = "[CQ:image,file=base64://" + base64 + "]"
                data = (
                    "标题:"
                    + setu_title
                    + "\npid:"
                    + str(setu_pid)
                    + "\n画师:"
                    + setu_author
                )
            else:
                return "Error:", f"获取图片失败! 错误码: {base64}", False
            return pic, data, True, setu_url

        except Exception as e:
            logger.warning("{}".format(e))
            if "额度限制" not in res.text:
                return "Error:", f"图库中没有搜到关于{keyword}的图。", False
            else:
                return "Error:", e, False
        except httpx.HTTPError as e:
            logger.warning("{}".format(e))
            return "Error:", f"API异常{e}", False

async def downPic(url,r18) -> str:
    proxies = {
        "http://": "http://192.168.0.49:7890",
        "https://": "http://192.168.0.49:7890",
    }
    async with AsyncClient(proxies=proxies) as client:
        headers = {
            "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            ba = str(base64.b64encode(re.content))
            pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
            logger.info("成功获取图片")
            await save_img(re,r18)
            return pic
        else:
            logger.error(f"获取图片失败: {re.status_code}")
            return re.status_code


if __name__ == "__main__":
    downPic(ghs_pic3())
