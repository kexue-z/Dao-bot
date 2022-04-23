FROM xana278/ubuntu-playwright-cn-python-docker-image

COPY  pyproject.toml /
COPY  poetry.lock /

RUN poetry config virtualenvs.create false \
  && poetry export --without-hashes -f requirements.txt \
  | poetry run python3.9 -m pip install -r /dev/stdin

WORKDIR /nonebot
