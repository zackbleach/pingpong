from app import api, auth
from app.resources.pingpong_resource import PingPongResource
from app.helpers.swagger_models import token
from flask import g

namespace = api.namespace("token")


@namespace.route('/')
class Token(PingPongResource):

    @auth.login_required
    @api.marshal_with(token)
    def get(self):
        token = g.api_user.generate_auth_token()
        return dict(token=token.decode('ascii'))
