from app import app
from app.repository.player_repository import get_player_by_id
from app.services.trueskill_service import get_chance_of_draw
from config import API_PATH
from flask import jsonify

CHANCE_API_PATH = API_PATH + '/' + "chance"


@app.route(CHANCE_API_PATH + '/<player_one_id>/<player_two_id>',
           methods=['GET'])
def quality(player_one_id, player_two_id):
    player_one = get_player_by_id(player_one_id)
    player_two = get_player_by_id(player_two_id)
    chance_of_draw = get_chance_of_draw(player_one, player_two)
    return jsonify(chance_of_draw=chance_of_draw)
