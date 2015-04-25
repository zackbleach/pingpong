from flask.ext.restplus import fields
from app import api

pagination = api.model('Pagination', {
    'page': fields.Integer(required=False, description='Page'),
    'page_size': fields.Integer(required=True, description='Page Size'),
    'total': fields.Integer(required=True, description='Total')
    })
