FROM python:3.11-bookworm
LABEL authors="Clément Besnier"


WORKDIR /

COPY . /src

RUN apt-get update; apt-get install nodejs

RUN pip install -r /src/requirements.txt

ENTRYPOINT ["top", "-b"]