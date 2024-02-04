FROM python:3.11-bookworm
LABEL authors="Clément Besnier"


WORKDIR /

COPY . /src
WORKDIR /src
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN apt-get update; apt-get install -y nodejs python3-venv virtualenv python3-virtualenv
RUN python3 -m venv /sat_venv && source /sat_venv/bin/activate
RUN /sat_venv/bin/pip3 install -r /src/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/src/"
ENV PYTHONUNBUFFERED 1
ENV FLASK_ENV development
RUN chmod +x /src/sat_biblio_server/scripts/script_import_all_documents.py && /sat_venv/bin/python3 /src/sat_biblio_server/scripts/script_import_all_documents.py
ENTRYPOINT ["top", "-b"]