FROM ubuntu:latest

ENV LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN.UTF-8 \
    LC_CTYPE=zh_CN.UTF-8 \
    LC_ALL=zh_CN.UTF-8 \
    TZ=Asia/Shanghai \
    DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --fix-missing \
    python3 python3-pip locales locales-all fonts-noto language-pack-zh-hans 

RUN apt install -y tzdata \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo ${TZ} > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

RUN python3 -m pip install poetry playwright \
    && playwright install chromium \
    && apt-get install -y libnss3-dev libxss1 libasound2 libxrandr2 \
    libatk1.0-0 libgtk-3-0 libgbm-dev libxshmfence1 \
    && apt clean autoclean \
    && apt autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# RUN apt update && apt install -y libzbar0 git wget
RUN apt update && apt install -y git wget

COPY ./pyproject.toml ./poetry.lock* /

RUN poetry config virtualenvs.create false
RUN poetry export -f requirements.txt --output /requirements.txt --without-hashes
RUN poetry run python3 -m pip install -r /requirements.txt

RUN wget https://github.com/ianfab/Fairy-Stockfish/releases/latest/download/fairy-stockfish-largeboard_x86-64 -O /tmp/fairy-stockfish

WORKDIR /nonebot

RUN git clone https://github.com/kexue-z/dao-bot.git .
