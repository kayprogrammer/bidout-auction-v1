FROM python:3.11-slim-buster

RUN apt-get update && \
    apt-get install -y postgresql-client

# Our Debian with Python and Nginx for python apps.
# See https://hub.docker.com/r/nginx/unit/
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./initial.sh /docker-entrypoint.d/initial.sh

RUN chmod +x /docker-entrypoint.d/initial.sh

RUN mkdir build

# We create folder named build for our app.
WORKDIR /build

COPY ./ ./
COPY ./.env .
COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN chmod +x ./initial.sh

CMD ["bash", "./initial.sh"]

ENV PYTHONPATH=/build
