"""
Override Django settings for jbei_lead_web project in development environment.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""


from ftf_web.settings.base import *
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# read in .env file
environ.Env.read_env()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
SITE_DOMAIN = 'localhost:7000'
SITE_ID = 3

# Static files
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'staticfiles')
)

DATABASES = {
    'default': env.db('SECRET_LOCAL_PG_DB_URL'),
    'local': env.db('SECRET_LOCAL_PG_DB_URL'),
    'aws': env.db('SECRET_AWS_PG_DB_URL'),
    'ese': env.db('SECRET_ESE_PG_DB_URL'),
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "http"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'request_logging.middleware.LoggingMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
