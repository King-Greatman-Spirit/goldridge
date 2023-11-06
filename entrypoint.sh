#!/bin/sh
# /opt/venv/bin/python manage.py dumpdata < webstacka.json
# /opt/venv/bin/python manage.py dumpdata --natural-foreign --natural-primary -e auth.permission -e contenttypes > webstacka.json
# /opt/venv/bin/python manage.py migrate --run-syncdb

# find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
# find . -path "*/migrations/*.pyc"  -delete

# /opt/venv/bin/python manage.py remove_stale_contenttypes
/opt/venv/bin/python manage.py makemigrations
/opt/venv/bin/python manage.py migrate
# /opt/venv/bin/python manage.py showmigrations
# /opt/venv/bin/python manage.py flush
# /opt/venv/bin/python manage.py dbshell < sqlite_db_dump.sql

# /opt/venv/bin/python manage.py loaddata webstacka.json
/opt/venv/bin/python manage.py collectstatic --no-input
/opt/venv/bin/python  manage.py test --no-input
# /opt/venv/bin/python manage.py createsuperuser


/opt/venv/bin/gunicorn goldridge.wsgi:application --bind 0.0.0.0:8000


