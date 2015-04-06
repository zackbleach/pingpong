from app import auth
from app.repository.api_user_repository import get_api_user_by_username
from flask import abort


@auth.verify_password
def verify_password(username, password):
    try:
        api_user = get_api_user_by_username(username)
    except ValueError:
        return False
    return api_user.verify_password(password)


@auth.error_handler
def auth_error():
    abort(401)
