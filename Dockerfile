FROM docker.io/library/python:3.9.9-slim-buster

WORKDIR /app

COPY . /app/

RUN pip install . && pip cache purge

ENV ALLOW_PORT=5006
ENV ALLOW_HOST=localhost
CMD ["bash", "-c", "bokeh serve --port ${ALLOW_PORT} --allow-websocket-origin ${ALLOW_HOST}:${ALLOW_PORT} notebooks/fractall.py"]