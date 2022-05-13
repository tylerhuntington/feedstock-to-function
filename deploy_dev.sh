###
# Shell script for spinning up FTF site for local dev, bypassing Docker.
###
export DJANGO_SETTINGS_MODULE=ftf_web.settings.development \
    &&
python manage.py makemigrations --merge \
    && python manage.py migrate \
    && echo yes | python manage.py collectstatic \
    && python manage.py runserver 0.0.0.0:7000 
