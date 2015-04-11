from app import app, db, Config
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer,
                          SignatureExpired, BadSignature)
from passlib.apps import custom_app_context as pwd_context


class ApiUser(db.Model):

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(Config.SECRET_KEY, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        if not token:
            return None
        s = Serializer(app.config.SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = ApiUser.query.get(data['id'])
        return user
