FROM python:3.10.6-slim as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /fastapiapp

ARG uid=1000
ARG guid=$uid
ARG user=fastapiuser

RUN groupadd -g ${guid} ${user} &&  \
    useradd --no-log-init -r -u ${uid} -g ${guid} ${user}

COPY requirements.txt /fastapiapp
RUN pip install -r requirements.txt

COPY entrypoint.sh /entry/
RUN chmod +x /entry/entrypoint.sh

COPY --chown=${uid} . .

USER ${user}

EXPOSE 8000

ENTRYPOINT /entry/entrypoint.sh
