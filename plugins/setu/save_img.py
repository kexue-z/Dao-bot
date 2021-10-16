import aiofiles
import glob
from httpx import AsyncClient


async def save_img(response, r18):
    index = len(glob.glob(f"./data/setu/{'r18/' if r18 else ''}*.jpg"))
    img_path = f"data/setu/{'r18/' if r18 else ''}" + str(index) + ".jpg"
    async with aiofiles.open(img_path, "wb") as f:
        try:
            await f.write(response.content)
        except TimeoutError:
            pass


async def upload_img(url: str, base64: str, apikey: str) -> str:
    params = {"key" : apikey, "source": base64}
    async with AsyncClient() as client:
        await client.get(url=url, params=params)
