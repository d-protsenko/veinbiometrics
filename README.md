# Finger vein biometrics

* [Description](#description)
* [Technology stack](#technology-stack)
* [How to run](#how-to-run)
    * [Requirements](#requirements)
    * [Important notice](#important-notice)
    * [Running in development mode](#running-in-development-mode)

## Description

This is a project of __biometric recognition by finger vein pattern__.

## Technology stack

* Python3.6
* Django
* OpenCV
* MongoDB

## How to run

### Requirements

Install packages using pip (for python 3.6):
* Pillow
* django
* djongo
* opencv-python
* numpy
* matplotlib

### Important notice

**You must change default database name and username/password pair before using app!**

Files to change:

- _[Makefile](./Makefile) (only for mongodb in Docker)_
- _[docker-compose.yml](./dev-env/docker-compose.yml) (only for mongodb in Docker)_

### Running in development mode

1) Install [Docker](http://docker.io) (≥ 18.09.7-ce)
2) Install [Docker Compose](https://docs.docker.com/compose) (≥ 1.17.1)
3) Install [Make](https://www.gnu.org/software/make)
4) Run following command in project root folder:

```console
$ make init_db
$ make start_server
```
