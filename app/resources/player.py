from app import api, db
from app import auth
from app.services.player_service import player_exists, player_exists_by_email
from app.repository.player_repository import (get_players,
                                              get_player_by_id,
                                              store_player,
                                              update_player,
                                              delete_player)
from app.resources.pingpong_resource import PingPongResource
from app.helpers.parsers import PlayerParser
from app.helpers.swagger_models import player, player_paginated

namespace = api.namespace("players")


@namespace.route("/", endpoint='Players')
@api.doc(responses={401: 'Not Authorised'})
class PlayerList(PingPongResource):

    @api.marshal_with(player_paginated)
    @auth.login_required
    def get(self):
        pagination = self.get_pagination()
        players = get_players(pagination)
        return self.paginated_result_to_json(players)

    @api.marshal_with(player)
    @api.expect(player)
    @auth.login_required
    @api.doc(responses={201: 'Player Created'})
    def post(self):
        parser = PlayerParser()
        player = parser.parse()
        self.abort_if_player_with_email_exists(player.email)
        store_player(player)
        db.session.commit()
        return player

    def abort_if_player_with_email_exists(self, email):
        if player_exists_by_email(email):
            message = 'Player with email address: %r already exists'
            raise ValueError(message % email)


@namespace.route("/" + '<int:id>')
@api.doc(responses={401: 'Not Authorised'}, params={'id': 'ID of the player'})
class PlayerSingle(PingPongResource):

    @api.marshal_with(player)
    @auth.login_required
    def get(self, id):
        return get_player_by_id(id)

    @auth.login_required
    @api.marshal_with(player)
    @api.expect(player)
    @api.doc(responses={201: 'Player Updated'})
    def put(self, id):
        self.abort_if_player_does_not_exist(id)
        parser = PlayerParser()
        player = parser.parse()
        player.id = id
        update_player(player)
        db.session.commit()
        return get_player_by_id(id), 201

    @auth.login_required
    @api.doc(responses={204: 'Player Deleted'})
    def delete(self, id):
        self.abort_if_player_does_not_exist(id)
        delete_player(id)
        db.session.commit()
        return '', 204

    def abort_if_player_does_not_exist(self, id):
        if not player_exists(id):
            message = 'Player with ID: %d does not exist'
            raise ValueError(message % id)
