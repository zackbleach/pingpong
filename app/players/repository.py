from app import db
from app.players.model import Player
from sqlalchemy import and_, desc, asc


def get_player_by_id(id):
    player = Player.query.filter_by(id=id).first()
    if player is None:
        raise ValueError('Player with ID: %d not found' % id)
    return player


def get_player_by_google_id(google_id):
    player = Player.query.filter_by(google_id=google_id).first()
    return player


def get_players(pagination, ordering, **kwargs):
    order_by_column = get_order_by_column(ordering)
    query = get_player_filter_query(**kwargs)
    players = (query.order_by(order_by_column)
                    .paginate(pagination.page,
                              pagination.page_size,
                              False))
    return players


def get_player_filter_query(**kwargs):
    query = Player.query
    office = kwargs.get('office', None)
    if (office is not None):
        query = query.filter(Player.office == office)
    return query


def get_player_by_email(email):
    player = Player.query.filter_by(email=email).first()
    if player is None:
        raise ValueError('Player with Email: %s not found' % email)
    return player


def store_player(player):
    db.session.add(player)


def store_players(players):
    for player in players:
        db.session.add(player)


def get_players_with_skill_above(player_id, number_of_players):
    player = get_player_by_id(player_id)

    aboves = (Player.query
              .filter(and_(
                      Player.skill >= player.skill,
                      Player.id != player_id,
                      Player.office == player.office)
                      )
              .order_by(desc(Player.skill))
              .limit(number_of_players).all())

    if aboves:
        aboves = [above.to_json() for above in aboves]

    return aboves


def get_players_with_skill_below(player_id, number_of_players):
    player = get_player_by_id(player_id)

    belows = (Player.query
              .filter(and_(
                      Player.skill < player.skill,
                      Player.id != player_id,
                      Player.office == player.office)
                      )
              .order_by(desc(Player.skill))
              .limit(number_of_players).all())

    if belows:
        belows = [below.to_json() for below in belows]

    return belows


def update_player(player):
    (db.session.query(Player).filter(Player.id == player.id)
                             .update({'first_name': player.first_name,
                                      'last_name': player.last_name}))


def delete_player(player_id):
    (db.session.query(Player).filter(Player.id == player_id).delete())


def get_order_by_column(ordering):
    if (ordering is None):
        return Player.id
    fields = Player.__dict__
    column = None
    if (ordering.direction == 'desc'):
        column = desc(fields.get(ordering.order_by))
    else:
        column = asc(fields.get(ordering.order_by))
    return column
