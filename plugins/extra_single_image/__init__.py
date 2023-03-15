import base64

from httpx import HTTPError, AsyncClient
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment

url = "http://192.168.0.29:7860/sdapi/v1/extra-single-image"


async def run_com(img_bytes: bytes, anime: bool):
    str_img = str(base64.b64encode(img_bytes), "utf-8")
    data = {
        "resize_mode": 0,
        "show_extras_results": True,
        "gfpgan_visibility": 0,
        "codeformer_visibility": 0,
        "codeformer_weight": 0,
        "upscaling_resize": 4,
        "upscaling_resize_w": 512,
        "upscaling_resize_h": 512,
        "upscaling_crop": False,
        "upscaler_1": "R-ESRGAN 4x+ Anime6B" if anime else "R-ESRGAN 4x+",
        "upscaler_2": "None",
        "extras_upscaler_2_visibility": 0,
        "upscale_first": False,
        "image": str_img,
    }

    async with AsyncClient() as client:
        re = await client.post(url=url, data=data)
        if img := re.json()["image"]:
            return img
        else:
            return


extra_images = on_command("超分", aliases={"超分辨", "超分辨率"})


async def get_img(url):
    async with AsyncClient() as client:
        try:
            re = await client.get(url)
            return re.content
        except HTTPError:
            return


@extra_images.handle()
async def _(
    event: MessageEvent,
):
    if event.reply:
        img = event.reply.message["image"][0]
        img_url = str(img.data.get("url", ""))
        if "a" in event.get_plaintext() or len(event.get_plaintext()) == 0:
            anime = True
        else:
            anime = False

        if img_url:
            img = await get_img(img_url)
            if img:
                if resp_img := await run_com(img, anime):
                    await extra_images.finish(MessageSegment.image(resp_img))
                else:
                    await extra_images.finish("Error")

            else:
                await extra_images.finish("Error")

    else:
        await extra_images.finish("用回复格式哦")
