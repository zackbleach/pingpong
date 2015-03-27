from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import restful

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
api = restful.Api(app)
db = SQLAlchemy(app)

from controllers.players_controller import Player
api.add_resource(Player, '/player')
