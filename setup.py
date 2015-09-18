import sys
from setuptools import setup


required = ['pyserial']

if sys.version_info[:2] < (3, 4):
    required.append('enum34')

setup(

    name = "PyCOZIR",
    version = '0.1',
    packages = ['cozir'],

    install_requires = required,

    author = "Pierre Haessig",
    author_email = "pierre.haessig@crans.org",

    description = 'a Python interface to COZIR CO2 sensors',

    license = 'BSD-3',

    url = 'https://github.com/pierre-haessig/pycozir',

)
