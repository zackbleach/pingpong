from app import db
from passlib.apps import custom_app_context as pwd_context


class ApiUser(db.Model):

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password)
