![yamdb](https://github.com/lexlibman/yamdb_final/workflows/yamdb/badge.svg?branch=master)

[![Python](https://img.shields.io/badge/-Python-464646??style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646??style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646??style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![NGINX](https://img.shields.io/badge/-NGINX-464646??style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![docker](https://img.shields.io/badge/-Docker-464646??style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646??style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

#API_YaMDB

It's api for my learning project. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

[docker](https://docs.docker.com/engine/install/) <br>
[docker-compose](https://docs.docker.com/compose/install/)

### Installing

A step by step series of examples that tell you have to get a development env running

Environment variables what you need are in `.env` file, but you need to add `POSTGRES_PASSWORD`

Put they to .env and set yours values

Say what the step will be

```
$ docker compose up
$ docker exec -it <CONTAINER ID> bash
```
### Next commands will be executed in the container:

Collect static to STATIC_ROOT

```
$ python manage.py collectstatic
```

Migrate to database

```
$ python manage.py migrate
```

Create superuser

```
$ python manage.py createsuperuser
```

Example of initializing start data

```
$ python manage.py loaddata fixtures.json
```

### Site is working on: 
* [130.193.57.79:5003/admin/](http://130.193.57.79:5003/admin/)

### Documentation:
* [130.193.57.79:5003/redoc/](http://130.193.57.79:5003/redoc/)

### API:
* [130.193.57.79:5003/api/v1/](http://130.193.57.79:5003/api/v1/)

## Running the tests

Use [pytest](https://docs.pytest.org/en/stable/)

Tests check settings of Django, dockerfile, docker-compose ane requirements

## Project powered by:
* [Python 3.8.5](https://www.python.org/downloads/release/python-385/) <br>
* [Django 3.0.8](https://www.djangoproject.com) <br>
* [Django Rest Framework 3.11.0](https://www.django-rest-framework.org) <br>
* [Simple JWT 4.3.0](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

## Authors

**Aleksei Libman** - *Initial work* - (https://github.com/lexlibman)

## License [![BSDv3 license](https://img.shields.io/badge/License-BSDv3-blue.svg)](LICENSE.md)

This project is licensed under the BSD 3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Yandex.Praktikum
