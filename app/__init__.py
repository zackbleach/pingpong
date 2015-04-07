from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()


'''
Add support for Database migrations with alembic
'''

from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


'''
Import all the views so routes will work
'''
from app.views import errors, extended_game_view, extended_player_view, token_view
