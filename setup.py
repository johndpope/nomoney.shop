"""https://github.com/pypa/sampleproject/blob/master/setup.py"""
from setuptools import setup, find_packages
from os import path
from config.settings import VERSION

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='nomoney.shop',
    version=VERSION,
    description='Plattform to exchange goods and services and calculate possible deals direct and indirect',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/snake-soft/nomoney.shop',

    author='Snake-Soft',
    author_email='info@snake-soft.com',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: System :: Filesystems',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='moneyless exchange platform',

    packages=find_packages(exclude=[]),

    python_requires='!=2.*, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',

    install_requires=['django',],


    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage', 'pylint'],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/snake-soft/nomoney.shop/issues/',
        'Source': 'https://github.com/snake-soft/nomoney.shop',
    },
)