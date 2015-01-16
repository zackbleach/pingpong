from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(models.Player, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(models.Game, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(models.PlayerGameMap, methods=['GET', 'POST', 'PUT', 'DELETE'])
