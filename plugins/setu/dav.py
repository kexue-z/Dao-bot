from io import BytesIO

from httpx import AsyncClient as httpx_client
from nonebot import get_driver
from webdav4.client import Client as dav_client

setu_dav_url = get_driver().config.setu_dav_url
setu_dav_username = get_driver().config.setu_dav_username
setu_dav_password = get_driver().config.setu_dav_password


def upload_file(file_obj, pid: str, p: str, r18: bool = False):
    client = dav_client(
        setu_dav_url,
        auth=(setu_dav_username, setu_dav_password),
    )
    client.upload_fileobj(
        file_obj, to_path=f"setu{'r18' if r18 else '' }/{pid}_{p}.jpg", overwrite=True
    )


def convert_file(bytes_file):
    file = BytesIO(bytes_file)
    return file


def save_img(content, pid: str, p: str, r18: bool = False):
    upload_file(convert_file(content), pid, p, r18)
