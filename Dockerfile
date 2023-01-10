FROM docker.io/library/python:3.9.9-slim-buster

RUN pip install poetry \
    && pip cache purge --no-input \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY . /app/

RUN poetry install --no-ansi --no-interaction

ENV ALLOW_PORT=5006
ENV ALLOW_HOST=localhost

CMD ["bash", "-c", "bokeh serve --port ${ALLOW_PORT} --allow-websocket-origin ${ALLOW_HOST}:${ALLOW_PORT} run/fractall.py"]