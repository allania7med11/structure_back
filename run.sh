#!/bin/sh
echo "envs $1 $2"
python manage.py makemigrations
python manage.py migrate 
if [ "$1" = "dev" ]; then
    python manage.py collectstatic --noinput
    python manage.py runserver $2
else
    gunicorn shop_back.wsgi:application --bind 0.0.0.0:$2
fi
