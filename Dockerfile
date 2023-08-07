FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN pip install --upgrade pip
RUN apt-get install -y ncat

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv &&  \
    pipenv install --system --deploy --ignore-pipfile

COPY . .

COPY ./fastapi-entrypoint.sh /fastapi-entrypoint.sh

RUN chmod +x /fastapi-entrypoint.sh
