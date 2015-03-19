from app import db
from sqlalchemy.sql import and_
import datetime


class Participant(db.Model):
    collection_name = 'participants'
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    winner = db.Column(db.Boolean)


class Player(db.Model):
    collection_name = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(120), nullable=False)
    skill = db.Column(db.Float, default=25)
    skill_sd = db.Column(db.Float, default=8.333333333333334)
    office = db.Column(db.Enum('San Francisco',
                               'Brighton',
                               'Berlin',
                               'New York',
                               'Stuttgart'), nullable=False)

    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    email=self.email,
                    avatar=self.avatar,
                    skill=self.skill,
                    skill_sd=self.skill_sd,
                    office=self.office
                    )


def __repr__(self):
        return '<User %r>' % (self.name)


class Game(db.Model):
    collection_name = 'games'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    loser_score = db.Column(db.Integer, nullable=False)
    losers = db.relationship('Player',
                             secondary=Participant.__table__,
                             secondaryjoin=and_(
                                 Player.id == Participant.player_id,
                                 Participant.winner == False))
    winners = db.relationship('Player',
                              secondary=Participant.__table__,
                              secondaryjoin=and_(
                                  Player.id == Participant.player_id,
                                  Participant.winner == True))

    def to_json(self):
        return dict(id=self.id,
                    date=self.date,
                    loser_score=self.loser_score,
                    loser=[l.to_json() for l in self.loser],
                    winner=[w.to_json() for w in self.winner]
                    )

    def __repr__(self):
        return '<Game %r>' % (self.id)
