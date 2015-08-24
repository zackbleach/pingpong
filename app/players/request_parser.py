from app import api, Config
from app.players.model import Player
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
        player_parser.add_argument('google_id',
                                   type=str,
                                   required=True,
                                   location='json')
        player_parser.add_argument('email',
                                   type=str,
                                   required=False,
                                   location='json')
        self.parser = player_parser

    def parse(self):
        parsed_body = self.parser.parse_args()
        return Player(first_name=parsed_body.first_name,
                      last_name=parsed_body.last_name,
                      nick_name=parsed_body.nick_name,
                      avatar=parsed_body.avatar,
                      office=parsed_body.office,
                      google_id=parsed_body.google_id,
                      email=parsed_body.email)
