from app import api, auth, db
from app.helpers.parsers import GameParser
from app.helpers.swagger_models import game as game_model
from app.helpers.swagger_models import game_paginated
from app.repository.game_repository import (get_games,
                                            store_game_and_get_id,
                                            get_game_by_id,
                                            get_games_since_days,
                                            get_games_for_player_since_days)
from app.resources.paginated_resource import PaginatedResource
from app.services.participant_service import store_participants_from_game
from app.services.player_service import update_players_skill_from_game
from app.services.skill_history_service import store_skill_histories_from_game

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
    def get(self):
        pagination = self.get_pagination()
        days = self.get_days()
        player_id = self.get_player_id()
        days_exists = days is not None and days != 0
        player_id_exists = player_id is not None and player_id != 0
        games = None
        if (days_exists and player_id_exists):
            games = get_games_for_player_since_days(player_id,
                                                    days,
                                                    pagination)
        elif (days_exists):
            games = get_games_since_days(days, pagination)
        else:
            games = get_games(pagination)
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
