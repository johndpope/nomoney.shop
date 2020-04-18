"""
Cut out important data from git repository
base.py holds all default data
data.py holds all private data (needs to be copied from data_sample.py first
"""
from .base import *
from .data import ALLOWED_HOSTS, DEBUG, SECRET_KEY
