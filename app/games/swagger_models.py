from app import api
from app.pagination.swagger_models import pagination
from app.players.swagger_models import player
from flask.ext.restplus import fields


game = api.model('Game', {
    'id': fields.Integer(required=False, description='Game ID'),
    'loser_score': fields.Integer(required=False, description='Loser Score'),
    'date': fields.String(required=True, description='Date'),
    'winners': fields.Nested(player, 'winners'),
    'losers': fields.Nested(player, 'player')
    })


game_paginated = api.extend('Game Paginated',
                            pagination,
                            {'results': fields.Nested(game, 'Game')})
