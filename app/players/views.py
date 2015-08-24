from app import api, db
from app import auth
from app.players.service import player_exists, player_exists_by_email
from app.players.repository import (get_players,
                                    get_player_by_id,
                                    store_player,
                                    update_player,
                                    delete_player,
                                    get_player_by_google_id)
from app.pagination.paginated_resource import (PaginatedResource, paginated)
from app.players.request_parser import PlayerParser
from app.players.swagger_models import player, player_paginated
from config import Config
from flask_restful import abort
import logging

namespace = api.namespace("players")


@namespace.route("/exists", endpoint='Player Exists')
@api.doc(responses={401: 'Not Authorised'})
class PlayerExists(PaginatedResource):

    @auth.login_required
    @api.doc(params={'google_id': 'Google ID of player'})
    @paginated
    @api.marshal_with(player)
    def get(self):
        google_id = self.get_google_id()
        player = get_player_by_google_id(google_id)
        if player is None:
            abort(404, message="Player not found")
        return player

    def get_google_id(self):
        google_id_arg = 'google_id'
        parser = api.parser()
        parser.add_argument(google_id_arg, type=str, location="args")
        args = parser.parse_args()
        google_id = args.get(google_id_arg)
        if (google_id is None):
            abort(400, message="You must supply a google id")
        return google_id


@namespace.route("/", endpoint='Players')
@api.doc(responses={401: 'Not Authorised'})
class PlayerList(PaginatedResource):

    @api.marshal_with(player_paginated)
    @auth.login_required
    @api.doc(params={'office': 'Office players are in'})
    @paginated
    def get(self):
        pagination = self.get_pagination()
        ordering = self.get_ordering()
        office = self.get_office()
        players = get_players(pagination, ordering,
                              office=office)
        return self.paginated_result_to_json(players)

    def get_office(self):
        office_arg = 'office'
        parser = api.parser()
        parser.add_argument(office_arg, type=str, location="args")
        args = parser.parse_args()
        office = args.get(office_arg)
        if (office is not None and office not in Config.OFFICES):
            abort(400, message="Office not found")
        return office

    @api.marshal_with(player)
    @api.expect(player)
    @auth.login_required
    @api.doc(responses={201: 'Player Created'})
    def post(self):
        logging.debug('posting player')
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
class PlayerSingle(PaginatedResource):

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
