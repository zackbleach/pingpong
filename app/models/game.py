from app import db
from app.models.player import Player
from app.models.participant import Participant
from app.repository.player_repository import get_player_by_id
from sqlalchemy.sql import and_
import datetime


class Game(db.Model):
    collection_name = 'games'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    loser_score = db.Column(db.Integer, nullable=False)
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
                    date=self.date,
                    loser_score=self.loser_score,
                    losers=[loser.to_json() for loser in self.losers],
                    winners=[winner.to_json() for winner in self.winners]
                    )

    @staticmethod
    def from_json(json):
        winners, losers = Game.get_players_from_json(json)
        loser_score = json.get('loser_score')
        return Game(loser_score=loser_score,
                    winners=winners,
                    losers=losers)

    @staticmethod
    def get_players_from_json(game):
        winners = [get_player_by_id(winner['id'])
                   for winner in game.get('winners')]
        losers = [get_player_by_id(loser['id'])
                  for loser in game.get('losers')]

        return winners, losers

        def __repr__(self):
            return '<Game: id = %r>' % (self.id)
