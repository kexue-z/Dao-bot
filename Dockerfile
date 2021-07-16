FROM python

ENV TZ=Asia/Shanghai

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN pip install nb-cli \
nonebot-adapter-cqhttp \
nonebot-plugin-status \
ujson \
nonebot-plugin-cocdicer \
nonebot-plugin-wordbank \
nonebot-plugin-picsearcher \
nonebot-plugin-manager \
bilibili-api \
pillow

RUN nb plugin install nonebot_hk_reporter

RUN echo "deb http://mirrors.aliyun.com/debian/ buster main contrib non-free\ndeb http://mirrors.aliyun.com/debian/ buster-updates main contrib non-free" > /etc/apt/sources.list
RUN apt-get update && apt-get install -y fonts-wqy-microhei chromium

COPY requirements.txt /
RUN pip install -r requirements.txt 

RUN nb plugin install nonebot_plugin_gamedraw
RUN nb plugin install nonebot_plugin_apscheduler
RUN pip install matplotlib 
COPY SIMHEI.ttf /usr/local/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf
RUN nb plugin install nonebot_plugin_statistical
RUN pip install dnspython

