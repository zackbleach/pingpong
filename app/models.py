from app import db
from sqlalchemy.orm import column_property
from sqlalchemy import select, func, and_

import datetime


class Participant(db.Model):
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    winner = db.Column(db.Boolean)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    avatar = db.Column(db.String(120))
    skill = db.Column(db.Integer)
    # win_count = column_property(
        # select([func.count(1)]).
        # where(and_(Participant.player_id == id,
                   # Participant.winner == True)).
        # correlate_except('game')
    # )


def __repr__(self):
        return '<User %r>' % (self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    loser_score = db.Column(db.Integer)
    players = db.relationship('Player',
                              secondary=Participant.__table__)
    winner = db.relationship('Player',
                             secondary=Participant.__table__,
                             primaryjoin=and_(id == Participant.game_id,
                                              Participant.winner == True),
                             viewonly=True)

    def __repr__(self):
        return '<Game %r>' % (self.id)
