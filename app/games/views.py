from app import api, auth, db
from app.games.request_parser import GameParser
from app.helpers.swagger_models import game as game_model
from app.helpers.swagger_models import game_paginated
from app.games.repository import (get_games,
                                  store_game_and_get_id,
                                  get_game_by_id)
from app.helpers.paginated_resource import PaginatedResource, paginated
from app.participants.service import store_participants_from_game
from app.players.service import update_players_skill_from_game
from app.skill.service import store_skill_histories_from_game

namespace = api.namespace("games")


@namespace.route("/<int:id>")
@api.doc(parmas={'id': 'ID of the game'}, responses={401: 'Not Authorised'})
class GameSingle(PaginatedResource):

    @auth.login_required
    @api.marshal_with(game_model)
    def get(self, id):
        return get_game_by_id(id)


@namespace.route("/")
@api.doc(responses={401: 'Not Authorised'})
class GameList(PaginatedResource):

    @auth.login_required
    @api.marshal_with(game_paginated)
    @api.doc(params={'days_back':
                     'Number of days back game must have occured in'})
    @api.doc(params={'player_id':
                     'Player ID to filter by'})
    @paginated
    def get(self):
        pagination = self.get_pagination()
        ordering = self.get_ordering()
        days = self.get_days()
        player_id = self.get_player_id()
        games = get_games(pagination, ordering, days=days, player_id=player_id)
        return self.paginated_result_to_json(games)

    @auth.login_required
    @api.expect(game_model)
    @api.marshal_with(game_model)
    @api.doc(responses={201: 'Game Created'})
    def post(self):
        parser = GameParser()
        game = parser.parse()
        game.id = None
        store_game_and_get_id(game)

        store_participants_from_game(game)
        store_skill_histories_from_game(game)
        update_players_skill_from_game(game)

        db.session.commit()
        return game

    def get_days(self):
        days_arg = 'days_back'
        parser = api.parser()
        parser.add_argument(days_arg, type=int, location="args")
        args = parser.parse_args()
        days = args.get(days_arg)
        return days

    def get_player_id(self):
        player_arg = 'player_id'
        parser = api.parser()
        parser.add_argument(player_arg, type=int, location="args")
        args = parser.parse_args()
        player_id = args.get(player_arg)
        return player_id
