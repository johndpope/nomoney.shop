from os import path, environ
from snakelib.string import remove_bad_chars
from configparser import ConfigParser
from django.core.management.utils import get_random_secret_key
from . import BASE_DIR

CONFIG_PATH = path.join(BASE_DIR, '.config.txt')

# [BASE]
SECRET_KEY = get_random_secret_key()
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1']

# [DATABASE]
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
    DEBUG = environ.get('DEBUG') == 'True'

if 'ALLOWED_HOSTS' in environ.keys():
    ALLOWED_HOSTS = environ.get('ALLOWED_HOSTS').split(',')


if path.isfile(CONFIG_PATH):
    _parser = ConfigParser()
    _parser.read(CONFIG_PATH)
    if _parser.has_section('BASE'):
        _base = _parser['BASE']
        SECRET_KEY = str(_base.get('SECRET_KEY') or
                         get_random_secret_key())
        if 'DEBUG' in _base:
            DEBUG = _base['DEBUG'] == 'True'
        if 'ALLOWED_HOSTS' in _base:
            ALLOWED_HOSTS = remove_bad_chars(
                _base['ALLOWED_HOSTS'], '\'[]" '
                ).split(',') or ALLOWED_HOSTS

    if _parser.has_section('DATABASE'):
        _database = _parser['DATABASE']
        for field in ['TYPE', 'NAME', 'USER', 'HOST', 'PORT']:
            if field in _database:
                DB_CONFIG[field] = str(_database[field]) or DB_CONFIG[field]

        if 'PASSWORD' in _parser['DATABASE']:
            DB_CONFIG['PASSWORD'] = str(_database['PASSWORD']) or DB_CONFIG['PASSWORD']

    else:
        DB_CONFIG = None

else:
    DB_CONFIG = None
