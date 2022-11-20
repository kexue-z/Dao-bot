FROM xana278/ubuntu-playwright-cn-python-docker-image

# RUN apt update && apt install -y libzbar0 git wget
RUN apt update && apt install -y git wget

COPY ./pyproject.toml ./poetry.lock* /

RUN poetry config virtualenvs.create false
RUN poetry export -f requirements.txt --output /requirements.txt --without-hashes
RUN poetry run python3 -m pip install -r /requirements.txt

RUN wget https://github.com/ianfab/Fairy-Stockfish/releases/latest/download/fairy-stockfish-largeboard_x86-64 -O /tmp/fairy-stockfish

WORKDIR /nonebot

RUN git clone https://github.com/kexue-z/dao-bot.git .
