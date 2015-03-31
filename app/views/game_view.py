import json
from app import app
from app import db
from app.models.game import Game
from app.repository.participant_repository import store_participants_from_game
from app.repository.player_repository import get_player_by_id
from app.services.trueskill_service import (update_players_skill_from_game,
                                            get_chance_of_draw)
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


@app.route(API_PATH+'/'+'draw'+'/<player_one_id>/<player_two_id>',
           methods=['GET'])
def quality(player_one_id, player_two_id):
    player_one = get_player_by_id(player_one_id)
    player_two = get_player_by_id(player_two_id)
    chance_of_draw = get_chance_of_draw(player_one, player_two)
    return jsonify(chance_of_draw=chance_of_draw)
