__author__ = 'vkostov'

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'AWS Product Advertising CLI',
    'author': 'Vasil Kostov',
    'version': '0.1',
    'name': 'aws-prod'
}

setup(**config)
