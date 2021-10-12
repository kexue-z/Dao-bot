FROM python:3.9

ENV TZ=Asia/Shanghai

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install poetry \
    && poetry config virtualenvs.create false

# RUN mkdir /nonebot && cd /nonebot 

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry export --without-hashes -f requirements.txt \
  | poetry run pip install -r /dev/stdin

WORKDIR /nonebot

# RUN pip install \

#     nb-cli \
#     nonebot-adapter-cqhttp \
#     nonebot-hk-reporter \
#     nonebot-plugin-gamedraw \
#     nonebot-plugin-apscheduler \
#     nonebot-plugin-statistical \
#     nonebot-plugin-cocdicer \
#     nonebot-plugin-wordbank \
#     nonebot-plugin-picsearcher \
#     nonebot-plugin-manager \
#     nonebot-plugin-test \
#     nonebot-plugin-trpglogger \
#     nonebot_plugin-puppet \
#     nonebot-plugin-heweather

# RUN pip install ujson \
#     bilibili-api \
#     pillow \
#     dnspython \
#     aiofiles \
#     pypinyin \
#     matplotlib \
#     wolframalpha

# RUN pip install brotlipy





