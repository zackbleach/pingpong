import json
from app import app
from app import db
from app.models.game import Game
from app.services.participant_service import store_participants_from_game
from app.services.player_service import update_players_skill_from_game
from config import API_PATH
from flask import request
from flask import jsonify


GAME_API_PATH = API_PATH + '/' + Game.collection_name


@app.route(GAME_API_PATH, methods=['POST'])
def store_game():
    game_json = json.loads(request.data)
    game = Game.from_json(game_json)
    db.session.add(game)
    db.session.flush()  # get games ID

    store_participants_from_game(game)
    update_players_skill_from_game(game)

    db.session.commit()
    return jsonify(game=game.to_json())
