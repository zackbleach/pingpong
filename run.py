from config import API_PATH
from app import app, db, auth
from flask.ext.restless import APIManager
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

from app.models.game import Game
from app.models.player import Player
from app.services import player_service, game_service
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


api_manager.create_api(Player,
                       collection_name=Player.collection_name,
                       methods=['GET', 'POST', 'PUT', 'DELETE'],
                       url_prefix=API_PATH,
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
                       url_prefix=API_PATH)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from app.views import extended_game_view, extended_player_view, errors, token_view
from app.models import api_user

app.debug = True

if __name__ == '__main__':
    manager.run()
