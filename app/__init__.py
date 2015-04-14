from config import Config
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask.ext.restplus import Api

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
auth = HTTPBasicAuth()
api = Api(app, version='3.0', title='Pingpong Rankings')


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


from app.services.authorisation_service import verify_password
from app.resources.pingpong_resource import PingPongResource
from app.resources.player import PlayerList, PlayerSingle
from app.resources.game import GameSingle, GameList
from app.resources.skill import SkillHistory, SkillClosest
from app.resources.token import Token
