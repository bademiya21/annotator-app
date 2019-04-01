FROM python:3.6-alpine

RUN adduser -D text-annotator

WORKDIR /home/annotator_app

RUN apk upgrade --update \
	&& apk add --no-cache openblas libgcc libstdc++ \
	&& apk add --no-cache --virtual build-runtime python3-dev gcc gfortran freetype-dev musl-dev openblas-dev g++

COPY requirements.txt requirements.txt
RUN python3 -m venv venv
RUN venv/bin/pip3 install --no-cache-dir numpy
RUN venv/bin/pip3 install --no-cache-dir -r requirements.txt
RUN venv/bin/pip3 install --no-cache-dir gunicorn

RUN apk del build-runtime

COPY application application
COPY migrations migrations
COPY annotator_app.py config.py boot.sh .env ./
RUN chmod a+x boot.sh

ENV FLASK_APP annotator_app.py

RUN chown -R text-annotator:text-annotator ./
USER text-annotator

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
