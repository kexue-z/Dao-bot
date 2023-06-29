FROM python:3.11-bullseye as requirements-stage

WORKDIR /tmp

RUN curl -sSL https://pdm.fming.dev/dev/install-pdm.py | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml ./pdm.lock* /tmp/

RUN pdm export -f requirements --output requirements.txt --without-hashes

FROM python:3.11-bullseye as build-stage

WORKDIR /wheel

COPY --from=requirements-stage /tmp/requirements.txt /wheel/requirements.txt

RUN pip wheel --wheel-dir=/wheel --no-cache-dir --requirement /wheel/requirements.txt

FROM python:3.11-slim-bullseye

WORKDIR /nonebot

ENV TZ Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

# RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

COPY --from=build-stage /wheel /wheel

RUN pip install --no-cache-dir --no-index --find-links=/wheel -r /wheel/requirements.txt && rm -rf /wheel

RUN playwright install --with-deps chromium


# FROM python:3.11

# # ENV LANG=zh_CN.UTF-8 \
# #     LANGUAGE=zh_CN.UTF-8 \
# #     LC_CTYPE=zh_CN.UTF-8 \
# #     LC_ALL=zh_CN.UTF-8 \
# #     TZ=Asia/Shanghai \
# #     DEBIAN_FRONTEND=noninteractive

# RUN apt update && apt install -y --fix-missing \
#     locales locales-all fonts-noto libnss3-dev libxss1 libasound2 libxrandr2 libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1

# RUN apt install -y tzdata \
#     && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
#     && echo ${TZ} > /etc/timezone \
#     && dpkg-reconfigure -f noninteractive tzdata

# # RUN python3 -m pip install playwright \
# #     && playwright install chromium \
# #     && apt-get install -y libnss3-dev libxss1 libasound2 libxrandr2 \
# #     libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1 \
# #     && apt clean autoclean \
# #     && apt autoremove -y \
# #     && rm -rf /var/lib/apt/lists/*

# # RUN apt update && apt install -y libzbar0 git wget
# # RUN apt update && apt install -y git wget

# COPY requirements.txt /

# RUN python3 -m pip install -r /requirements.txt

# RUN playwright install --with-deps chromium

# WORKDIR /nonebot

COPY ./plugins/ /nonebot/plugins/
COPY ./utils/ /nonebot/utils/
COPY ./bot.py /nonebot/bot.py