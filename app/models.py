from app import db


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    avatar = db.Column(db.String(120))

    def __repr__(self):
        return '<User %r>' % (self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    def __repr__(self):
        return '<Game %r>' % (self.id)


class PlayerGameMap(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    score = db.Column(db.Integer)
