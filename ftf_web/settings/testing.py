"""
Override Django settings for jbei_lead_web project in testing environment.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

from jbei_lead_web.settings.base import *
import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# read in .env file
environ.Env.read_env()

APP_ENVIRONMENT = 'testing'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Static files
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'staticfiles')
)

# File system storage for large files (serialized models, reference data, etc)
FILE_STORE_ROOT = os.path.join(BASE_DIR, 'jbei_lead_file_store')
SPLEARN_MODEL_FILES = os.path.join(FILE_STORE_ROOT, 'model_files', 'splearn')
SUPERPRO_MODEL_FILES = os.path.join(FILE_STORE_ROOT, 'model_files', 'superpro')

DATABASES = {
    'heroku': env.db('HEROKU_PG_DB_URL'),
    'default': env.db('AWS_PG_DB_URL'),
    'ese': env.db('ESE_PG_DB_URL'),
}

# Deployment configs
LOAD_PLINES_ON_DEPLOY = False
