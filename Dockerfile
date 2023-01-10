FROM docker.io/library/python:3.9.9-slim-buster

WORKDIR /app

COPY . /app/

RUN pip install . && pip cache purge

CMD ["bokeh", "serve", "notebooks/fractall.py"]