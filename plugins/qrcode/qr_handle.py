from httpx import AsyncClient


api_url = "https://api.iyk0.com/qr"


async def get_qr_data(url: str) -> str:

    async with AsyncClient() as client:
        params = {"imgurl": url}
        try:
            res = await client.get(url=api_url, timeout=10, params=params)

            qrtext = res.json()["qrtext"]
            return qrtext
        except:
            pass
