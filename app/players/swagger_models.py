from flask.ext.restplus import fields
from app.pagination.swagger_models import pagination
from app import api
from app import Config


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
