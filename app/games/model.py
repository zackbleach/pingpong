from app import db
from app.players.model import Player
from app.participants.model import Participant
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.sql import and_


class Game(db.Model):
    collection_name = 'games'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    loser_score = db.Column(db.Integer, nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('player.id'))
    losers = db.relationship('Player',
                             secondary=Participant.__table__,
                             secondaryjoin=and_(
                                 Player.id == Participant.player_id,
                                 Participant.winner == False),
                             viewonly=True)
    winners = db.relationship('Player',
                              secondary=Participant.__table__,
                              secondaryjoin=and_(
                                  Player.id == Participant.player_id,
                                  Participant.winner == True),
                              viewonly=True)

    def to_json(self):
        return dict(id=self.id,
                    date=str(self.date),
                    submitted_by=self.submitted_by,
                    loser_score=self.loser_score,
                    losers=[loser.to_json() for loser in self.losers],
                    winners=[winner.to_json() for winner in self.winners]
                    )

    def get_players(self):
        return self.winners + self.losers

    @validates('date')
    def check_date_in_past(self, key, date):
        now = datetime.utcnow()
        if date is None or date > now:
            raise ValueError('Date must not be in the future')
        return date

    def __repr__(self):
        return '<Game: id = %r>' % (self.id)
