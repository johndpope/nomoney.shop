from os import path, environ
from configparser import ConfigParser
from django.core.management.utils import get_random_secret_key
from . import BASE_DIR

CONFIG_PATH = path.join(BASE_DIR, '.config.txt')

#[BASE]
SECRET_KEY = get_random_secret_key()
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

#[DATABASE]
DB_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': '',
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    }

if 'SECRET_KEY' in environ.keys():
    SECRET_KEY = str(environ.get('SECRET_KEY'))

if 'DEBUG' in environ.keys():
    DEBUG = eval(environ.get('DEBUG'))

if 'ALLOWED_HOSTS' in environ.keys():
    ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(',')


if path.isfile(CONFIG_PATH):
    _parser = ConfigParser()
    _parser.read(CONFIG_PATH)
    if _parser.has_section('BASE'):
        _base = _parser['BASE']
        SECRET_KEY = str(_base.get(SECRET_KEY) or
                         get_random_secret_key())
        if 'DEBUG' in _base:
            DEBUG = eval(_base['DEBUG'])
        if 'ALLOWED_HOSTS' in _base:
            ALLOWED_HOSTS = eval(_base['ALLOWED_HOSTS']) or ALLOWED_HOSTS

    if _parser.has_section('DATABASE'):
        _database = _parser['DATABASE']
        if 'TYPE' in _database:
            DB_CONFIG['TYPE'] = str(_database['TYPE']) or DB_CONFIG['TYPE']
        if 'NAME' in _parser['DATABASE']:
            DB_CONFIG['NAME'] = str(_database['NAME']) or DB_CONFIG['NAME']
        if 'USER' in _parser['DATABASE']:
            DB_CONFIG['USER'] = str(_database['USER']) or DB_CONFIG['USER']
        if 'PASSWORD' in _parser['DATABASE']:
            DB_CONFIG['PASSWORD'] = str(_database['PASSWORD']) or DB_CONFIG['PASSWORD']
        if 'HOST' in _parser['DATABASE']:
            DB_CONFIG['HOST'] = str(_database['HOST']) or DB_CONFIG['HOST']
        if 'PORT' in _parser['DATABASE']:
            DB_CONFIG['PORT'] = str(_database['PORT']) or DB_CONFIG['PORT']
    else:
        DB_CONFIG = None

else:
    DB_CONFIG = None
