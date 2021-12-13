FROM python:3.9

ENV TZ=Asia/Shanghai
ENV LANG zh_CN.UTF-8
ENV LANGUAGE zh_CN.UTF-8
ENV LC_ALL zh_CN.UTF-8
ENV TZ Asia/Shanghai
ENV DEBIAN_FRONTEND noninteractive

COPY sources.list /etc/apt/sources.list

RUN apt update && apt install -y libzbar0 locales locales-all fonts-noto

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install poetry \
    && poetry config virtualenvs.create false

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry export --without-hashes -f requirements.txt \
    | poetry run pip install -r /dev/stdin

RUN playwright install chromium && playwright install-deps 

WORKDIR /nonebot
