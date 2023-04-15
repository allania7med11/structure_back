#!/bin/sh
echo "envs $ENVIRONMENT $PORT"
python manage.py makemigrations
python manage.py migrate 
if [ "$ENVIRONMENT" = "dev" ]; then
    python manage.py collectstatic --noinput
    python manage.py runserver $PORT
elif [ "$ENVIRONMENT" = "test" ]; then
    python manage.py collectstatic --noinput
    while :; do sleep 2073600; done
else
    gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
fi
