FROM python:3.9.7-slim-bullseye

RUN mkdir /bot

WORKDIR /bot

COPY pyproject.toml poetry.lock /bot/

RUN pip install "poetry==1.1.0"

RUN poetry config virtualenvs.create false && poetry install

COPY bot /bot

ENTRYPOINT ["python", "-m", "bot"]