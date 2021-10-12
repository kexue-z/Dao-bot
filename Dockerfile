FROM python:3.9

ENV TZ=Asia/Shanghai

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple \
    && pip install poetry \
    && poetry config virtualenvs.create false

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry export --without-hashes -f requirements.txt \
    | poetry run pip install -r /dev/stdin

WORKDIR /nonebot
