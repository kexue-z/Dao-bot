import base64
from re import findall
from sys import exc_info

import httpx
from httpx import AsyncClient
from nonebot import logger

from .dav import *


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
            content = await downPic(setu_url)
            setu_pid = res.json()["data"][0]["pid"]
            setu_author = res.json()["data"][0]["author"]
            p = res.json()["data"][0]["p"]

            base64 = convert_b64(content)
            save_img(content, pid=setu_pid, p=p, r18=r18)

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
            return pic, data, True, setu_url
        except httpx.ProxyError as e:
            logger.warning(e)
            return "Error:", f"代理错误: {e}", False
        except IndexError as e:
            logger.warning(e)
            return "Error:", f"图库中没有搜到关于{keyword}的图。", False
        except:
            logger.warning({exc_info()[0]}, {exc_info()[1]})
            return "Error:", f"{exc_info()[0]} {exc_info()[1]}。", False


async def downPic(url) -> str:
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
            # pic = convert_b64(re.content)
            logger.info("成功获取图片")
            # save_img(re.content, r18)
            return re.content
        else:
            logger.error(f"获取图片失败: {re.status_code}")
            return re.status_code


def convert_b64(content) -> str:
    ba = str(base64.b64encode(content))
    pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
    return pic


if __name__ == "__main__":
    downPic(ghs_pic3())
