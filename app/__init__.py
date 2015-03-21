from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import controllers

from models import Player
from models import Game
from config import API_PATH

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(Player,
                   collection_name=Player.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)

manager.create_api(Game,
                   collection_name=Game.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)
