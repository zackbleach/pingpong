from app import app, db, auth
from flask.ext.restless import APIManager

'''
Initial set up of the Restless API and adding of authentication to it
Verify password method has to be imported here for authentication
decorator trick (hack) to work.
'''

from app.services.authorisation_service import verify_password


@auth.login_required
def do_auth(*args, **kwargs):
    pass

api_manager = APIManager(app,
                         flask_sqlalchemy_db=db,
                         preprocessors=dict(GET_SINGLE=[do_auth],
                                            GET_MANY=[do_auth],
                                            PUT_SINGLE=[do_auth],
                                            PUT_MANY=[do_auth],
                                            POST=[do_auth],
                                            DELETE_SINGLE=[do_auth],
                                            DELETE_MANY=[do_auth]))

'''
Set up API endpoints for Player and Game models.
Also adds preprocessing methods to them to validate and
clean up incomming JSON
'''

from app.models.game import Game
from app.models.player import Player
from app.services import player_service, game_service


api_manager.create_api(Player,
                       collection_name=Player.collection_name,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       url_prefix=app.config.get('API_PATH'),
                       preprocessors={
                           'PUT_SINGLE': [player_service.pre_process_for_put],
                           'POST': [player_service.pre_process_for_post]
                       },
                       max_results_per_page=500)

api_manager.create_api(Game,
                       collection_name=Game.collection_name,
                       methods=['GET', 'PUT', 'DELETE'],
                       preprocessors={
                           'POST': [game_service.pre_process_for_post]
                       },
                       url_prefix=app.config.get('API_PATH'))


from app.views import errors, extended_game_view, extended_player_view, token_view
