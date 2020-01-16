FROM python:3.7.4
MAINTAINER Max Bridgland <mabridgland@protonmail.com>

RUN mkdir -p /usr/src/slacky
WORKDIR /usr/src/app

ADD requirements.txt /usr/src/app/requirements.txt

RUN pip install -r requirements.txt

RUN apt-get install python-opencv

ADD . /usr/src/app

CMD python -m slacky