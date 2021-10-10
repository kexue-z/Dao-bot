from nonebot.log import logger
from httpx import AsyncClient
import nonebot

apikey = nonebot.get_driver().config.qweather_apikey
if not apikey:
    raise ValueError(f"请在环境变量中添加 qweather_apikey 参数")
url_weather_api = "https://devapi.qweather.com/v7/weather/"
url_geoapi = "https://geoapi.qweather.com/v2/city/"


# 获取城市ID
async def get_Location(city_kw: str, api_type: str = "lookup") -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_geoapi + api_type, params={"location": city_kw, "key": apikey}
        )
        return res.json()


# 获取天气信息
async def get_WeatherInfo(api_type: str, city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_api + api_type, params={"location": city_id, "key": apikey}
        )
        return res.json()


# 获取天气灾害预警
async def get_WeatherWarning(city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            "https://devapi.qweather.com/v7/warning/now",
            params={"location": city_id, "key": apikey},
        )
        res = res.json()
    return res if res["code"] == "200" and res["warning"] else None


# 获取天气信息
async def get_City_Weather(city: str):
    # global city_id
    city_info = await get_Location(city)
    logger.debug(city_info)
    if city_info["code"] == "200":
        city_id = city_info["location"][0]["id"]
        city_name = city_info["location"][0]["name"]

        # 3天天气
        daily_info = await get_WeatherInfo("3d", city_id)
        daily = daily_info["daily"]
        day1 = daily[0]
        day2 = daily[1]
        day3 = daily[2]

        # 实时天气
        now_info = await get_WeatherInfo("now", city_id)
        now = now_info["now"]

        # 天气预警信息
        warning = await get_WeatherWarning(city_id)
        
        return {
            "city": city_name,
            "now": now,
            "day1": day1,
            "day2": day2,
            "day3": day3,
            "warning": warning,
        }
    else:
        logger.error(
            f"错误: {city_info['code']} 请参考 https://dev.qweather.com/docs/start/status-code/ "
        )
