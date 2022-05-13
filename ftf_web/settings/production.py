"""
Override Django settings for jbei_lead_web project in production environment.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from ftf_web.settings.base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# read in .env file
environ.Env.read_env()

APP_ENVIRONMENT = 'production'
SITE_DOMAIN = 'feedstock-to-function.lbl.gov'
SITE_ID = 1

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')


DATABASES = {
    'default': env.db('SECRET_ESE_PG_DB_URL'),
    'ese': env.db('SECRET_ESE_PG_DB_URL'),
    'aws': env.db('SECRET_AWS_PG_DB_URL'),
    'local': env.db('SECRET_LOCAL_PG_DB_URL'),
}
