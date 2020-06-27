from os import path
from configparser import ConfigParser
from django.core.management.utils import get_random_secret_key
from . import BASE_DIR

CONFIG_PATH = path.join(BASE_DIR, '.config.txt')

#[BASE]
SECRET_KEY = ''
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


if path.isfile(CONFIG_PATH):
    _parser = ConfigParser()
    _parser.read(CONFIG_PATH)
    if _parser.has_section('BASE'):
        SECRET_KEY = str(_parser['BASE'].get(SECRET_KEY) or
                         get_random_secret_key())
        if 'DEBUG' in _parser['BASE']:
            DEBUG = eval(_parser['BASE']['DEBUG'])
        if 'ALLOWED_HOSTS' in _parser['BASE']:
            ALLOWED_HOSTS = eval(_parser['BASE']['ALLOWED_HOSTS']) or ALLOWED_HOSTS

    if _parser.has_section('DATABASE'):
        if 'TYPE' in _parser['DATABASE']:
            DB_CONFIG['TYPE'] = str(_parser['DATABASE']['TYPE']) or DB_CONFIG['TYPE']
        if 'NAME' in _parser['DATABASE']:
            DB_CONFIG['NAME'] = str(_parser['DATABASE']['NAME']) or DB_CONFIG['NAME']
        if 'USER' in _parser['DATABASE']:
            DB_CONFIG['USER'] = str(_parser['DATABASE']['USER']) or DB_CONFIG['USER']
        if 'PASSWORD' in _parser['DATABASE']:
            DB_CONFIG['PASSWORD'] = str(_parser['DATABASE']['PASSWORD']) or DB_CONFIG['PASSWORD']
        if 'HOST' in _parser['DATABASE']:
            DB_CONFIG['HOST'] = str(_parser['DATABASE']['HOST']) or DB_CONFIG['HOST']
        if 'PORT' in _parser['DATABASE']:
            DB_CONFIG['PORT'] = str(_parser['DATABASE']['PORT']) or DB_CONFIG['PORT']
    else:
        DB_CONFIG = None

else:
    DB_CONFIG = None
