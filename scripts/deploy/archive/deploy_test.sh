###
# Shell script for spinning up JBEI LEAD site for local dev, bypassing Docker.
###
export DJANGO_SETTINGS_MODULE=jbei_lead_web.settings.testing \
    &&
python manage.py makemigrations --merge \
    && python manage.py migrate \
    && echo yes | python manage.py collectstatic \
    && python manage.py runserver 0.0.0.0:7000 
