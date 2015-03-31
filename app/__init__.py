from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('config')
app.config['DEBUG'] = True
db = SQLAlchemy(app)


import views.game_view
import views.chance_view

from app.models.player import Player
from app.models.game import Game
from config import API_PATH

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Player,
                   collection_name=Player.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)

manager.create_api(Game,
                   collection_name=Game.collection_name,
                   methods=['GET', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)
