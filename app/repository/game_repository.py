from app import db
from app.models.participant import Participant
from app.models.game import Game
from sqlalchemy import desc


def get_games_for_player(player_id):
    games = (db.session.query(Game, Participant)
               .join(Participant)
               .filter(Participant.player_id == player_id)
               .order_by(desc(Game.id))
               .all())
    return games


def get_game_by_id(id):
    game = db.session.query(Game).filter(Game.id == id).first()
    if game is None:
        raise ValueError('Game with ID: %d not found' % id)
    return game


def get_games(pagination):
    games = Game.query.paginate(pagination.page,
                                pagination.page_size,
                                False)
    return games


def store_game_and_get_id(game):
    db.session.add(game)
    db.session.flush()
