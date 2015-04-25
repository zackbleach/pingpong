from app import api, auth
from app.helpers.swagger_models import skill_history_paginated, chance_of_draw, skill_closest
from app.helpers.parsers.skill_parsers import (SkillHistoryParser,
                                               SkillClosestParser,
                                               SkillDrawParser)
from app.services.player_service import get_chance_of_draw
from app.repository.player_repository import (get_players_with_skill_above,
                                              get_players_with_skill_below)
from app.repository.skill_history_repository import get_history_for_player_from_date
from app.resources.paginated_resource import PaginatedResource
from datetime import datetime, timedelta


namespace = api.namespace("skill")


@namespace.route("/history/<int:player_id>")
class SkillHistory(PaginatedResource):

    @auth.login_required
    @api.doc(params={'player_id': 'Player ID to get Skill History for',
                     'days': 'How many days to retrieve history for'},
             responses={401: 'Not Authorised'})
    @api.marshal_with(skill_history_paginated)
    def get(self, player_id):
        parser = SkillHistoryParser()
        days = parser.parse()
        from_date = datetime.utcnow() - timedelta(days=days)
        pagination = self.get_pagination()
        history = get_history_for_player_from_date(player_id,
                                                   from_date,
                                                   pagination)
        return self.paginated_result_to_json(history)


@namespace.route("/draw/")
class SkillDraw(PaginatedResource):

    @auth.login_required
    @api.doc(params={'player_one_id': 'Player One',
                     'player_two_id': 'Player Two'},
             responses={401: 'Not Authorised'})
    @api.marshal_with(chance_of_draw)
    def get(self):
        parser = SkillDrawParser()
        player_one_id, player_two_id = parser.parse()
        chance_of_draw = get_chance_of_draw(player_one_id,
                                            player_two_id)

        return dict(chance_of_draw=chance_of_draw)


@namespace.route("/closest/<int:player_id>")
class SkillClosest(PaginatedResource):

    @auth.login_required
    @api.doc(params={'number_of_players': 'Number of Players'},
             responses={401: 'Not Authorised'})
    @api.marshal_with(skill_closest)
    def get(self, player_id):
        parser = SkillClosestParser()
        no_players = parser.parse()

        above = get_players_with_skill_above(player_id, no_players)
        below = get_players_with_skill_below(player_id, no_players)

        return dict(above=above,
                    below=below)
