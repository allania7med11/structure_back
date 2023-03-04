#!/bin/sh
echo "envs $ENVIRONMENT $PORT"
python manage.py makemigrations
python manage.py migrate 
if [ "$ENVIRONMENT" = "dev" ]; then
    python manage.py collectstatic --noinput
    python manage.py runserver $PORT
else
    gunicorn server.wsgi:application --bind 0.0.0.0:$PORT
fi
