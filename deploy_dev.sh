#!/usr/bin/env bash

echo "making migration"
python manage.py migrate
echo "sleeping for 5 sec"
sleep 5
echo "waking up"
echo "collecting static"
python manage.py collectstatic --noinput
#echo "update airport"
#echo "rebuild index"
# python manage.py rebuild_index --noinput
#python manage.py loaddata fixtures/*.json
echo "exposing server"
gunicorn bizrefpro.wsgi -b 0.0.0.0:8000 -k gevent --workers=4 --log-level=debug
