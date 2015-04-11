from app import api, auth, db
from app.helpers.parsers import GameParser
from app.helpers.swagger_models import game as game_model
from app.helpers.swagger_models import game_paginated
from app.repository.game_repository import (get_games,
                                            store_game_and_get_id,
                                            get_game_by_id)
from app.resources.pingpong_resource import PingPongResource
from app.services.participant_service import store_participants_from_game
from app.services.player_service import update_players_skill_from_game
from app.services.skill_history_service import store_skill_histories_from_game

namespace = api.namespace("games")


@namespace.route("/<int:id>")
@api.doc(parmas={'id': 'ID of the game'}, responses={401: 'Not Authorised'})
class GameSingle(PingPongResource):

    @auth.login_required
    @api.marshal_with(game_model)
    def get(self, id):
        return get_game_by_id(id)


@namespace.route("/")
@api.doc(responses={401: 'Not Authorised'})
class GameList(PingPongResource):

    @auth.login_required
    @api.marshal_with(game_paginated)
    def get(self):
        pagination = self.get_pagination()
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
