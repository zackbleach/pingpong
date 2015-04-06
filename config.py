import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

API_VERSION = 2
API_PATH = '/api/' + str(API_VERSION)

PINGPONG_TOKEN_KEY = os.environ['PINGPONG_TOKEN_KEY']
