import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))
project_name = "pingpong"


class Config(object):
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    SECRET_KEY = os.urandom(24)

    API_VERSION = 2
    API_PATH = '/api/' + str(API_VERSION)

    DEFAULT_PAGE_SIZE = 25

    OFFICES = ['Brighton', 'New York', 'San Francisco',
               'London', 'Berlin', 'Stuttgart']


class Dev(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_ECHO = False
