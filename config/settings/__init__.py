"""
Cut out important data from git repository
base.py holds all default data
data.py holds all private data (needs to be copied from data_sample.py first
"""
from os import environ
from .base import *
try:
    import config.settings.data as DATA
except ModuleNotFoundError:
    DATA = False


DEFAULT_DATA = {
    'ALLOWED_HOSTS': [],
    'DEBUG': False,
    'SECRET_KEY': ''
    }

for attr, default in DEFAULT_DATA.items():
    if DATA and hasattr(DATA, attr):
        globals()[attr] = getattr(DATA, attr)
    elif environ.get(attr):
        globals()[attr] = environ.get(attr).split(',')
    else:
        globals()[attr] = DEFAULT_DATA.get(attr)
