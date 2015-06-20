from app import api
from app.pagination.swagger_models import pagination
from app.players.swagger_models import player
from flask.ext.restplus import fields


game = api.model('Game', {
    'id': fields.Integer(required=False, description='Game ID'),
    'loser_score': fields.Integer(required=False, description='Loser Score'),
    'winner_score': fields.Integer(required=False, description='Winner Score'),
    'submitted_by': fields.Integer(required=True,
                                   description='User ID of submitter'),
    'office': fields.String(required=True, description='Office'),
    'date': fields.String(required=True, description='Date'),
    'winners': fields.Nested(player, 'winners', required=True),
    'losers': fields.Nested(player, 'losers', required=True)
    })


game_paginated = api.extend('Game Paginated',
                            pagination,
                            {'results': fields.Nested(game, 'Game')})
