from config import API_PATH
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

manager = APIManager(app, flask_sqlalchemy_db=db)

from app.models.game import Game
from app.models.player import Player

manager.create_api(Player,
                   collection_name=Player.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH,
                   max_results_per_page=500)

manager.create_api(Game,
                   collection_name=Game.collection_name,
                   methods=['GET', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)
