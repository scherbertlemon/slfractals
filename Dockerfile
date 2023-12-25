FROM python:3.12-slim-bullseye AS base

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
    g++ \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv --upgrade-deps /pypoetry \
    && /pypoetry/bin/pip install poetry==1.7.1 \
    && /pypoetry/bin/pip cache purge --no-input

COPY --chmod=755 scripts/poetry /usr/local/bin

FROM base as environment

WORKDIR /slfractals
COPY poetry.lock pyproject.toml poetry.toml /slfractals/

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