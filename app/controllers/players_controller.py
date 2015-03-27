from flask.ext import restful
from app.repository import player_repository


class Player(restful.Resource):
    def get(self):
        return player_repository.get_players()
