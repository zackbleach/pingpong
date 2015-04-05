from app import app
from app.models.player import Player
from app.repository.game_repository import get_games_for_player
from app.repository.player_repository import (get_player_by_id,
                                              get_players_with_skill_above,
                                              get_players_with_skill_below)
from app.repository.skill_history_repository import get_history_for_player
from app.services.player_service import (get_chance_of_draw)
from config import API_PATH
from flask import jsonify


PLAYER_API_PATH = API_PATH + '/' + Player.collection_name


@app.route(PLAYER_API_PATH + '/<player_id>/games',
           methods=['GET'])
def games(player_id):
    games = get_games_for_player(player_id)
    games_json = [game.to_json() for game in games]
    return jsonify(games=games_json)


@app.route(PLAYER_API_PATH + '/<player_id>/skill',
           methods=['GET'])
def skill_history(player_id):
    skill_history = get_history_for_player(player_id)
    history = [skill.to_json() for skill in skill_history]
    return jsonify(skill_history=history)


@app.route(PLAYER_API_PATH + '/chances/<player_one_id>/<player_two_id>',
           methods=['GET'])
def draw(player_one_id, player_two_id):
    player_one = get_player_by_id(player_one_id)
    player_two = get_player_by_id(player_two_id)
    chance_of_draw = get_chance_of_draw(player_one, player_two)
    return jsonify(chance_of_draw=chance_of_draw)


@app.route(PLAYER_API_PATH + '/closest/<player_id>',
           defaults={'no_players': 1}, methods=['GET'])
@app.route(PLAYER_API_PATH + '/closest/<player_id>/<no_players>',
           methods=['GET'])
def closest_skill(player_id, no_players):
    above = get_players_with_skill_above(player_id, no_players)
    below = get_players_with_skill_below(player_id, no_players)
    return jsonify(above=above, below=below)
