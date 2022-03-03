# freeseat-api

API for application to connect people who require a lift with ones who can give it.

# Installation guide

Clone the repository
```shell
git clone https://github.com/freeseat/freeseat-api
```


Install [pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) and dependencies (macOS)
```shell
brew install openssl readline sqlite3 xz zlib

curl https://pyenv.run | bash

pyenv install 3.10.1
```


Install [poetry](https://python-poetry.org)
```shell
cd freeseat-api

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

source $HOME/.poetry/env

poetry config settings.virtualenvs.in-project true
```


```shell
pyenv local 3.10.1

poetry install

peotry shell
```


Install pre-commit
```shell
pre-commit install
```


### Create the database

```shell
psql postgres

create database freeseat;
create user username with encrypted password "password";
grant all privileges on database freeseat to username;
\q

psql freeseat
create extension postgis;
create extension postgis_topology;
\q
```


### Apply migrations

```shell
cd app
./manage.py migrate
```


### Create superuser

```shell
./manage.py createsuperuser
```


### Run the server

```shell
./manage.py runserver
```


### Running server in docker

```shell
docker-compose -f deployment/docker-compose.yml -p freeseat-api up --build --force-recreate -d
```


## List of the environmental variables used in project:

| Variable               | Default value      | Is required | Description                               |
|------------------------|--------------------|:-----------:| ----------------------------------------- |
| DJANGO_SECRET_KEY      |                    |     Yes     |                                           |
| DJANGO_DEBUG           | False              |     No      |                                           |
| POSTGRES_DB            | freeseat           |     No      |                                           |
| POSTGRES_HOST          | 127.0.0.1          |     No      |                                           |
| POSTGRES_PORT          | 5432               |     No      |                                           |
| POSTGRES_USER          |                    |     Yes     |                                           |
| POSTGRES_PASSWORD      |                    |     Yes     |                                           |
| DJANGO_SETTINGS_MODULE | core.settings_prod |     No      |                                           |
| SENTRY_DSN             |                    |     Yes     |                                           |
