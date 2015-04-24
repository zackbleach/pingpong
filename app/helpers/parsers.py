from app import api, Config
from app.models.game import Game
from app.models.player import Player
from app.repository.player_repository import get_player_by_id
from datetime import datetime
from flask_restful import inputs


class PlayerParser():

    def __init__(self):
        player_parser = api.parser()
        player_parser.add_argument('first_name',
                                   type=str,
                                   required=True,
                                   location='json')
        player_parser.add_argument('last_name',
                                   type=str,
                                   required=True,
                                   location='json')
        player_parser.add_argument('nick_name',
                                   type=str,
                                   required=True,
                                   location='json')
        player_parser.add_argument('avatar',
                                   type=inputs.url,
                                   required=True,
                                   location='json')
        player_parser.add_argument('office',
                                   type=inputs.regex('|'.join(Config.OFFICES)),
                                   location='json')
        player_parser.add_argument('email',
                                   type=str,
                                   required=True,
                                   location='json')
        self.parser = player_parser

    def parse(self):
        parsed_body = self.parser.parse_args()
        return Player(first_name=parsed_body.first_name,
                      last_name=parsed_body.last_name,
                      nick_name=parsed_body.nick_name,
                      avatar=parsed_body.avatar,
                      office=parsed_body.office,
                      email=parsed_body.email)


class GameParser():

    def __init__(self):
        parser = api.parser()
        parser.add_argument('id',
                            type=int,
                            required=False,
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
                    loser_score=body.loser_score,
                    winners=winners,
                    losers=losers)


class SkillHistoryParser():

    def __init__(self):
        parser = api.parser()
        parser.add_argument('days', type=int, location='args')
        self.parser = parser

    def parse(self):
        days = self.parser.parse_args().get('days')
        return days


class SkillDrawParser():

    def __init__(self):
        parser = api.parser()
        parser.add_argument('player_one_id',
                            type=int, location='args',
                            required=True)
        parser.add_argument('player_two_id',
                            type=int,
                            location='args',
                            required=True)
        self.parser = parser

    def parse(self):
        players = self.parser.parse_args()
        player_one_id = players.player_one_id
        player_two_id = players.player_two_id
        return player_one_id, player_two_id


class SkillClosestParser():

    def __init__(self):
        parser = api.parser()
        parser.add_argument('number_of_players',
                            type=int,
                            location='args',
                            default=1)
        self.parser = parser

    def parse(self):
        args = self.parser.parse_args()
        number_of_players = args.number_of_players
        return number_of_players
