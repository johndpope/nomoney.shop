"""
load environmental vars and base config
"""
from os import environ
from .base import *

try:
    import config.settings.data as DATA
except ImportError:
    DATA = False


DEBUG = environ.get('DEBUG') in ('True', 'true')
SECRET_KEY = environ.get('SECRET_KEY', '')
ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(',') \
    if 'ALLOWED_HOSTS' in environ else []
