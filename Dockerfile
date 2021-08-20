FROM python

ENV TZ=Asia/Shanghai

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

# RUN echo "deb http://mirrors.aliyun.com/debian/ buster main contrib non-free\ndeb http://mirrors.aliyun.com/debian/ buster-updates main contrib non-free" > /etc/apt/sources.list
# RUN apt-get update && apt-get install -y fonts-wqy-microhei chromium

RUN pip install \
    nb-cli \
    nonebot-adapter-cqhttp \
    # nonebot-hk-reporter \
    nonebot-plugin-gamedraw \
    nonebot-plugin-apscheduler \
    # nonebot-plugin-statistical \
    nonebot-plugin-cocdicer \
    nonebot-plugin-wordbank \
    nonebot-plugin-picsearcher \
    nonebot-plugin-manager \
    nonebot-plugin-test

RUN pip install ujson \
    bilibili-api \
    pillow \
    dnspython \
    aiofiles \
    pypinyin \
    matplotlib \
    wolframalpha

RUN pip install nonebot-plugin-trpglogger
RUN pip install nonebot_plugin_puppet
COPY SIMHEI.ttf /usr/local/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf



