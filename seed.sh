#!/bin/bash
rm -rf terraceapi/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations terraceapi
python manage.py migrate terraceapi
python manage.py loaddata users
python manage.py loaddata tokens