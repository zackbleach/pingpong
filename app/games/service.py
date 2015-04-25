import json
from app.games.repository import get_game_by_id
from flask import request


def game_exists(id):
    game = json.loads(request.data)
    game = get_game_by_id(id)
    return game is not None


def pre_process_for_post(data=None, **kw):
    fields = data.keys()
    if 'id' in fields:
        data['id'] = None
