#!/bin/sh

echo "ENVIRONMENT=$ENVIRONMENT"
echo "MIGRATE=$MIGRATE"
echo "COLLECTSTATIC=$COLLECTSTATIC"
echo "PORT=$PORT"

if [ "$MIGRATE" = "True" ]; then
    python manage.py migrate
fi

if [ "$COLLECTSTATIC" = "True" ]; then
    python manage.py collectstatic --noinput && echo "Generation completed successfully"
fi

if [ "$ENVIRONMENT" = "dev" ]; then
    python manage.py runserver 0.0.0.0:$PORT
elif [ "$ENVIRONMENT" = "debug" ]; then
    sleep infinity
else
    gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
fi