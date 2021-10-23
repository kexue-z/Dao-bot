from io import BytesIO

from httpx import AsyncClient as httpx_client
from nonebot import get_driver
from webdav4.client import Client as dav_client

setu_dav_url = get_driver().config.setu_dav_url
setu_dav_username = get_driver().config.setu_dav_username
setu_dav_password = get_driver().config.setu_dav_password


def upload_file(file_obj, r18: bool = False):
    client = dav_client(
        setu_dav_url,
        auth=(setu_dav_username, setu_dav_password),
    )
    if r18:
        id = len(client.ls("setur18", detail=False))
        client.upload_fileobj(file_obj, to_path=f"setur18/{id}.jpg")
    else:
        id = len(client.ls("setu", detail=False))
        client.upload_fileobj(file_obj, to_path=f"setu/{id}.jpg")


def convert_file(bytes_file):
    file = BytesIO(bytes_file)
    return file


def save_img(content, r18):
    upload_file(convert_file(content))


async def downPic(url):
    proxies = {
        "http://": "http://192.168.0.49:7890",
        "https://": "http://192.168.0.49:7890",
    }
    async with httpx_client(proxies=proxies) as client:
        headers = {
            "Referer": "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
    return re.content
