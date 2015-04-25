from app import api


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
