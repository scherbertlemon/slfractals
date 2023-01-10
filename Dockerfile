FROM docker.io/library/python:3.9.9-slim-buster

RUN pip install poetry \
    && pip cache purge --no-input \
    && poetry config virtualenvs.create false

WORKDIR /app

COPY . /app/

RUN poetry install --no-interaction
RUN jupyter contrib nbextension install --user \
    && jupyter nbextension enable splitcell/splitcell \
    && jupyter nbextension enable hide_input/main

ENV ALLOW_PORT=5006
ENV ALLOW_HOST=localhost

CMD ["bash", "-c", "bokeh serve --port ${ALLOW_PORT} --allow-websocket-origin ${ALLOW_HOST}:${ALLOW_PORT} run/fractall.py"]