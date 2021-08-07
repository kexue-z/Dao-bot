import base64
from re import findall

import nonebot
from nonebot import logger
from httpx import AsyncClient

__name__ = 'setu'

apikey = nonebot.get_driver().config.apikey
if nonebot.get_driver().config.setuproxy == 'True':
    proxy = 'i.pixiv.cat'
else:
    proxy = 'disable'


async def ghs_pic3(keyword='', r18=False) -> str:
    async with AsyncClient() as client:
        req_url = "https://api.lolicon.app/setu/"
        params = {'keyword': keyword,
                  'r18': 1 if r18 else 0
                  }
        res = await client.get(req_url, params=params)
        try:
            setu_title = res.json()['data'][0]['title']
            setu_url = res.json()['data'][0]['url']
            base64 = await downPic(setu_url)
            setu_pid = res.json()['data'][0]['pid']
            setu_author = res.json()['data'][0]['author']
            if base64:
                pic = "[CQ:image,file=base64://" + base64 + "]"
                data = "标题:" + setu_title + "\npid:" + str(
                    setu_pid) + "\n画师:" + setu_author
            logger.info(res.text)
            # return setu_url
            return pic, data, True
            # return pic
        except Exception as e:
            logger.warning('{}'.format(res.text))
            logger.warning('{}'.format(e))
            if '额度限制' not in res.text:
                return 'Error:' ,f"图库中没有搜到关于{keyword}的图。", False
            else:
                return 'Error:' ,e , False


async def downPic(url) -> str:
    async with AsyncClient() as client:
        headers = {
            'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
        re = await client.get(url=url, headers=headers, timeout=10)
        if re:
            ba = str(base64.b64encode(re.content))
            pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
            logger.info('成功获取图片')
            return pic


if __name__ == '__main__':
    downPic(ghs_pic3())
