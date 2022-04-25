FROM xana278/ubuntu-playwright-cn-python-docker-image

RUN apt update && apt install -y libzbar0 git

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry config virtualenvs.create false \
  && poetry export --without-hashes -f requirements.txt \
  | poetry run python3 -m pip install -r /dev/stdin

WORKDIR /nonebot

RUN git clone https://github.com/kexue-z/dao-bot.git .
