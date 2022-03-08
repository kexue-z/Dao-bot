from pathlib import Path
from anyio import open_file
from nonebot import on_keyword
from random import choice
from os import listdir
from nonebot.adapters.onebot.v11 import MessageSegment

JOKE_PATH = Path("./data/d2joke").absolute()

kw = {"命运笑话", "土命笑话", "D2笑话", "d2笑话"}

joke = on_keyword(kw, block=False)


@joke.handle()
async def handle_joke():
    file_list = listdir(str(JOKE_PATH))
    chosen = choice(file_list)
    async with await open_file(JOKE_PATH / chosen, "rb") as f:
        b = await f.read()

    await joke.finish(MessageSegment.image(b))
