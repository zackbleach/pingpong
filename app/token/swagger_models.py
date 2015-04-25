from flask.ext.restplus import fields
from app import api

token = api.model('Access Token', {
    'token': fields.String(required=True, description='Access Token'),
    })
