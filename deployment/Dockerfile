FROM python:3.10-slim

RUN mkdir /home/app
WORKDIR /home/app

COPY ../app/ ../poetry.lock ../pyproject.toml ../deployment/init_db.sh ./

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y git apt-utils binutils libpq-dev libproj-dev gdal-bin libcurl4-openssl-dev libssl-dev python3-dev python-dev libffi-dev build-essential && \
    apt-get clean

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install poetry==1.1.12

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

#CMD ["/bin/bash", "/home/app/init_db.sh"]
