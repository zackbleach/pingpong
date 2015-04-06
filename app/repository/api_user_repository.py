from app import db
from app.models.api_user import ApiUser


def get_api_user_by_username(username):
    user = (db.session.query(ApiUser)
                      .filter(ApiUser.username == username)
                      .first())
    if user is None:
        raise ValueError('User with name: %s not found' % username)
    return user
