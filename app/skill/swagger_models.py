from flask.ext.restplus import fields
from app import api
from app.pagination.swagger_models import pagination
from app.players.swagger_models import player


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
    'chance_of_draw': fields.Float(required=True,
                                   description='Chance of Players drawing \
                                   (between 0 and 1)')
    })


skill_closest = api.model('Closest in Skill', {
    'above': fields.Nested(player, required=True, description='Players'),
    'below': fields.Nested(player, required=True, description='Players'),
    })
