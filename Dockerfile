FROM xana278/ubuntu-playwright-cn-python-docker-image

RUN apt update && apt install -y libzbar0 git wget

COPY ./pyproject.toml ./poetry.lock* /

RUN poetry config virtualenvs.create false
RUN poetry export --without-hashes -f requirements.txt \
  | poetry run python3 -m pip install -r /dev/stdin

RUN wget https://github.com/ianfab/Fairy-Stockfish/releases/latest/download/fairy-stockfish-largeboard_x86-64 -O /tmp/fairy-stockfish

WORKDIR /nonebot

RUN git clone https://github.com/kexue-z/dao-bot.git .
