FROM python:3.9-slim-buster

MAINTAINER gvedevnet@cisco.com
USER 0
RUN umask 002

RUN apt-get update && apt-get -y install procps libnss-wrapper
RUN mkdir -p /app/logs

WORKDIR app

ADD requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

ADD . .

ENV FLASK_ENV development
ENV FLASK_APP app.py
ENV FLASK_DEBUG falseoc

EXPOSE 5000

CMD ["python","app.py"]