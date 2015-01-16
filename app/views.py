from app import app
import flask
import flask.ext.sqlalchemy
import flask.ext.restless

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)
