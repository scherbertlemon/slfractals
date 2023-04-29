FROM python:3.9-slim-bullseye AS environment

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry \
    && pip cache purge --no-input \
    && poetry config virtualenvs.create false

WORKDIR /slfractals
COPY poetry.lock pyproject.toml /slfractals/

RUN poetry install --no-interaction --no-ansi --no-root \
    && poetry cache clear --all --no-interaction .
RUN jupyter contrib nbextension install --user \
    && jupyter nbextension enable splitcell/splitcell \
    && jupyter nbextension enable hide_input/main

FROM environment AS application

COPY src /slfractals/src
RUN poetry install --no-interaction --no-ansi \
    && poetry cache clear --all --no-interaction .

ENV ALLOW_PORT=5006
ENV ALLOW_HOST=localhost

CMD ["bash", "-c", "bokeh serve --port ${ALLOW_PORT} --allow-websocket-origin ${ALLOW_HOST}:${ALLOW_PORT} src/fractal_app.py"]