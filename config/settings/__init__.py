"""
Cut out important data from git repository
base.py holds all default data
data.py holds all private data (needs to be copied from data_sample.py first
alternatively you can use environmentals
"""
from os import environ
from django.core.management.utils import get_random_secret_key
from .base import *
from .parser import SECRET_KEY, DEBUG, ALLOWED_HOSTS, DB_CONFIG


SQLITE_CONFIG = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
}

DATABASES = {
    'default': DB_CONFIG or SQLITE_CONFIG
}



#===============================================================================
# try:
#     import config.settings.data as DATA
# except ImportError:
#     DATA = False
#===============================================================================





#===============================================================================
# DEFAULT_DATA = {
#     'ALLOWED_HOSTS': [],
#     'DEBUG': False,
#     'SECRET_KEY': get_random_secret_key(),
#     }
# 
# for attr, default in DEFAULT_DATA.items():
#     if DATA and hasattr(DATA, attr):
#         globals()[attr] = getattr(DATA, attr)
#     elif environ.get(attr):
#         globals()[attr] = environ.get(attr).split(',')
#     else:
#         globals()[attr] = DEFAULT_DATA.get(attr)
#===============================================================================
