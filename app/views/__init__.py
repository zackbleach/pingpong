from app import manager
from app.models.player import Player
from app.models.game import Game
from config import API_PATH

manager.create_api(Player,
                   collection_name=Player.collection_name,
                   methods=['GET', 'POST', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)

manager.create_api(Game,
                   collection_name=Game.collection_name,
                   methods=['GET', 'PUT', 'DELETE'],
                   url_prefix=API_PATH)
