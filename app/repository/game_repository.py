from app import db
from app.models.participant import Participant
from app.models.game import Game
from datetime import date, timedelta
from sqlalchemy import desc, and_


def get_games_for_player_since_days(player_id, days, pagination):
    since_date = date.today() - timedelta(days=days)
    games = (Game.query
                 .join(Participant)
                 .filter(and_(
                         Participant.player_id == player_id,
                         Game.date > since_date)
                         )
                 .order_by(desc(Game.id))
                 .paginate(pagination.page,
                           pagination.page_size,
                           False))
    return games


def get_games_for_player(player_id, pagination):
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


def get_games_since_days(days, pagination):
    since_date = date.today() - timedelta(days=days)
    games = (Game.query.filter(Game.date > since_date)
                       .paginate(pagination.page,
                                 pagination.page_size,
                                 False))
    return games


def store_game_and_get_id(game):
    db.session.add(game)
    db.session.flush()
