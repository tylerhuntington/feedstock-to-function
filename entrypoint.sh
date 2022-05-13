#!/bin/bash

set -euxo pipefail

python3 manage.py migrate
python3 manage.py collectstatic --noinput
python3 manage.py loaddata accounts/init_fixtures/sites.json
python3 manage.py autocreatesuperuser
python3 manage.py updatechemfixtures

exec gunicorn ftf_web.wsgi -b 0.0.0.0:9000 -t 120
