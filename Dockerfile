FROM python:3.9.7-slim-bullseye

WORKDIR /bot

COPY pyproject.toml poetry.lock /bot/

RUN pip install "poetry==1.1.0" && \
 poetry config virtualenvs.create false && poetry install

COPY bot /bot/bot/

CMD ["python", "-m", "bot"]