from app import db
from app.models.participant import Participant
from app.games.model import Game
from datetime import date, timedelta
from sqlalchemy import desc, asc


def get_games(pagination, ordering, **kwargs):
    query = get_filter_query_for_game(**kwargs)
    games = (query.order_by(get_order_by_column(ordering))
                  .paginate(pagination.page,
                            pagination.page_size,
                            False))
    return games


def get_filter_query_for_game(**kwargs):
    query = Game.query
    query = get_player_id_query_if_exists(query, **kwargs)
    query = get_days_query_if_exists(query, **kwargs)
    return query


def get_player_id_query_if_exists(query, **kwargs):
    player_id = kwargs.get('player_id')
    if (player_id):
        query = query.filter(Participant.player_id == player_id)
    return query


def get_days_query_if_exists(query, **kwargs):
    days = kwargs.get('days')
    if (days):
        since_date = date.today() - timedelta(days=days)
        query = query.filter(Game.date > since_date)
    return query


def get_game_by_id(id):
    game = db.session.query(Game).filter(Game.id == id).first()
    if game is None:
        raise ValueError('Game with ID: %d not found' % id)
    return game


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


def get_order_by_column(ordering):
    if (ordering is None):
        return Game.id
    fields = Game.__dict__
    column = None
    if (ordering.direction == 'desc'):
        column = desc(fields.get(ordering.order_by))
    else:
        column = asc(fields.get(ordering.order_by))
    return column
