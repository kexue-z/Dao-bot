from httpx import AsyncClient
from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

miao = on_command("来个猫猫", aliases={"猫猫", "猫", "猫图"})


@miao.handle()
async def hf():
    async with AsyncClient() as client:
        img = await client.get("http://edgecats.net/")
    await miao.finish(MessageSegment.image(img.content))
