from app import api
from app.games.model import Game
from app.players.repository import get_player_by_id
from datetime import datetime


class GameParser():

    def __init__(self):
        parser = api.parser()
        parser.add_argument('id',
                            type=int,
                            required=False,
                            location='json')
        parser.add_argument('submitted_by',
                            type=int,
                            required=True,
                            location='json')
        parser.add_argument('loser_score',
                            type=int,
                            required=True,
                            location='json')
        parser.add_argument('winners',
                            type=list,
                            required=True,
                            location='json')
        parser.add_argument('losers',
                            type=list,
                            required=True,
                            location='json')
        self.parser = parser

    def get_players(self, players_from_body):
        players = []
        for player in players_from_body:
            id = player.get('id')
            if id is None:
                raise ValueError('Players must have an ID')
            else:
                players.append(get_player_by_id(id))
        return players

    def parse(self):
        body = self.parser.parse_args()
        winners = self.get_players(body.winners)
        losers = self.get_players(body.losers)
        return Game(id=body.id,
                    date=datetime.utcnow(),
                    submitted_by=body.submitted_by,
                    loser_score=body.loser_score,
                    winners=winners,
                    losers=losers)
