FROM python:3.10-slim

WORKDIR /home/user/web

COPY ./openssl.cnf .
ENV OPENSSL_CONF=/home/user/web/openssl.cnf
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /home/user/web/entrypoint.sh
RUN chmod +x /home/user/web/entrypoint.sh

COPY . .

ENTRYPOINT ["/home/user/web/entrypoint.sh"]