from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask.ext.restplus import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
api = Api(app, version='1.0', title='Pingpong Rankings')


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


from app.authorisation.authorisation_service import verify_password
from app.players.views import PlayerList, PlayerSingle
from app.games.views import GameSingle, GameList
from app.skill.views import SkillHistory, SkillClosest
from app.token.views import Token
