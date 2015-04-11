from flask.ext.restplus import fields
from app import api
from app import Config

pagination = api.model('Pagination', {
    'page': fields.Integer(required=False, description='Page'),
    'page_size': fields.Integer(required=True, description='Page Size'),
    'total': fields.Integer(required=True, description='Total')
    })


player = api.model('Player', {
    'id': fields.Integer(required=False, description='Player ID'),
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'nick_name': fields.String(required=True, description='Nick name'),
    'email': fields.String(required=True, description='Email'),
    'avatar': fields.String(required=True, description='Avatar'),
    'skill': fields.Float(required=True, description='Skill'),
    'skill_sd': fields.Float(required=True,
                             description='Skill Standard Deviation'),
    'office': fields.String(required=True, description='Office',
                            enum=[Config.OFFICES]),
    })


player_paginated = api.extend('Player Paginated',
                              pagination,
                              {'results': fields.Nested(player, 'Player')})


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


skill_history = api.model('Skill History', {
    'player_id': fields.Integer(required=False, description='Player ID'),
    'skill': fields.Float(required=True, description='Skill'),
    'skill_sd': fields.Float(required=True,
                             description='Skill Standard Deviation'),
    'date': fields.String(required=True, description='Date'),
    })


skill_history_paginated = api.extend('Skill history paginated',
                                     pagination,
                                     {'results': fields.Nested(skill_history,
                                                               'Skill History'
                                                               )})


chance_of_draw = api.model('Chance of Draw', {
    'player_one_id': fields.Integer(required=True, description='Player ID'),
    'player_two_id': fields.Integer(required=True, description='Player ID'),
    'chance_of_draw': fields.Float(required=True,
                                   description='Chance of Players drawing \
                                   (between 0 and 1)')
    })


skill_closest = api.model('Closest in Skill', {
    'above': fields.Nested(player, required=True, description='Players'),
    'below': fields.Nested(player, required=True, description='Players'),
    })


token = api.model('Access Token', {
    'token': fields.String(required=True, description='Access Token'),
    })
