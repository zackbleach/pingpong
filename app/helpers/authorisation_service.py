from app import auth
from app.api_user.model import ApiUser
from app.api_user.repository import get_api_user_by_username
from flask import abort, g, request


@auth.verify_password
def verify_password(username, password):
    token = request.args.get('token')
    if not token:
        try:
            api_user = get_api_user_by_username(username)
            if not api_user.verify_password(password):
                return False
        except ValueError:
            return False
    else:
        api_user = ApiUser.verify_auth_token(token)
    g.api_user = api_user
    return True


@auth.error_handler
def auth_error():
    abort(401)
