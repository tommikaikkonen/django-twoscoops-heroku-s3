"""Production settings and globals."""


from os import environ

from base import *

# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured

import herokuify

from herokuify.common import *              # Common settings, SSL proxy header
from herokuify.aws import *                 # AWS access keys as configured in env
from herokuify.mail.sendgrid import *       # ... or Sendgrid


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)

########## HOST CONFIGURATION
# See: https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['.herokuapp.com',]
########## END HOST CONFIGURATION


########## DATABASE CONFIGURATION
DATABASES = herokuify.get_db_config()       # Database config
########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = herokuify.get_cache_config()       # Cache config for Memcache/MemCachier
########## END CACHE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('SECRET_KEY')
########## END SECRET CONFIGURATION

#Storage on S3 settings are stored as os.environs to keep settings.py clean 
if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = environ['AWS_STORAGE_BUCKET_NAME']
    AWS_ACCESS_KEY_ID = environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = environ['AWS_SECRET_ACCESS_KEY']
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL
    AWS_PRELOAD_METADATA = True
