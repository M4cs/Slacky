FROM python:3.6.8
MAINTAINER Max Bridgland <mabridgland@protonmail.com>

RUN mkdir -p /usr/src/slacky
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

ADD . /usr/src/app

CMD python -m slacky