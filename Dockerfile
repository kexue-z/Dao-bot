FROM xana278/ubuntu-playwright-cn-python-docker-image

RUN apt update && apt install -y libzbar0

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry config virtualenvs.create false \
  && poetry export --without-hashes -f requirements.txt \
  | poetry run python3 -m pip install -r /dev/stdin

WORKDIR /nonebot
