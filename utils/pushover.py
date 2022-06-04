import time
from typing import Optional

from httpx import AsyncClient, Response, post

url = "https://api.pushover.net/1/messages.json"


async def async_send_message(
    message: str,
    token: str,
    user: str,
    device: Optional[str] = None,
    title: Optional[str] = None,
) -> Response:
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    params = {
        "token": token,
        "user": user,
        "message": message,
        "device": device if device else None,
        "title": title if title else message,
    }
    async with AsyncClient() as client:
        res = await client.post(url, headers=headers, timeout=10, params=params)
    return res


def sync_send_message(
    message: str,
    token: str,
    user: str,
    device: Optional[str] = None,
    title: Optional[str] = None,
) -> Response:
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    params = {
        "token": token,
        "user": user,
        "message": message,
        "device": device if device else None,
        "title": title if title else message,
    }
    res = post(url, headers=headers, timeout=10, params=params)
    return res


def send_startup_message(token, user):
    msg = "Bot 于 {} 启动".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    sync_send_message(msg, token, user, title="Bot 启动通知")
