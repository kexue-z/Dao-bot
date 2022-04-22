FROM docker.io/library/ubuntu:latest

ENV TZ=Asia/Shanghai
ENV LANG=zh_CN.UTF-8
ENV LANGUAGE=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y --fix-missing python3.9 python3-pip
RUN apt install -y --fix-missing language-pack-zh-hans libzbar0 locales locales-all fonts-noto 

RUN python3.9 -m pip install poetry \
  && poetry config virtualenvs.create false

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry export --without-hashes -f requirements.txt \
  | poetry run python3.9 -m pip install -r /dev/stdin

RUN playwright install-deps && playwright install chromium

WORKDIR /nonebot
