#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      echo $SQL_HOST
      echo $SQL_PORT
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

./manage.py flush --no-input
./manage.py migrate
./manage.py collectstatic

exec "$@"