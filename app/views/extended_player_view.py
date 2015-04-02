from app import app
from app.models.player import Player
from app.repository.player_repository import get_player_by_id
from app.services.player_service import get_players_above, get_players_below
from app.services.trueskill_service import get_chance_of_draw
from config import API_PATH
from flask import jsonify


PLAYER_API_PATH = API_PATH + '/' + Player.collection_name


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
    above = get_players_above(player_id, no_players)
    below = get_players_below(player_id, no_players)
    return jsonify(above=above, below=below)
