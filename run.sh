#!/bin/sh

echo "envs $ENVIRONMENT $PORT"
python manage.py makemigrations
python manage.py migrate

if [ "$COLLECTSTATIC" = "True" ]; then
    python manage.py collectstatic --noinput
fi

if [ "$ENVIRONMENT" = "dev" ]; then
    python manage.py runserver 0.0.0.0:$PORT
elif [ "$ENVIRONMENT" = "debug" ]; then
    sleep infinity
else
    gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
fi