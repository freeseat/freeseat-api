FROM python:3.10-slim as be

RUN apt-get update && \
    apt-get install -y git apt-utils binutils libpq-dev libproj-dev gdal-bin libcurl4-openssl-dev libssl-dev python3-dev python-dev libffi-dev build-essential && \
    apt-get clean

RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install poetry==1.1.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY app newrelic.ini ./

RUN python manage.py collectstatic --noinput

EXPOSE 8000

ENTRYPOINT ["NEW_RELIC_CONFIG_FILE=newrelic.ini", "newrelic-admin", "run-program", "gunicorn", "-w 3", "core.wsgi:application", "--bind=0.0.0.0:8000"]

FROM nginx:alpine as fe

COPY --from=be /app/static /var/www/static
COPY deployment/fe/nginx.conf /etc/nginx/conf.d/default.conf
