from config import API_PATH
from app import app, db
from flask.ext.restless import APIManager

manager = APIManager(app, flask_sqlalchemy_db=db)

from app.models.game import Game
from app.models.player import Player

manager.create_api(Player,
                   collection_name=Player.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH,
                   max_results_per_page=500)

manager.create_api(Game,
                   collection_name=Game.collection_name,
                   methods=['GET', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)


from app.views import extended_game_view, extended_player_view
app.debug = True
