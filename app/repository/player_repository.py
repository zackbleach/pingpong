from app import db
from app.models.player import Player
from sqlalchemy import and_, desc


def get_player_by_id(id):
    return Player.query.filter_by(id=id).first()


def get_players():
    players = Player.query.all()
    return [player.to_json() for player in players]


def store_player(player):
    db.session.add(player)
    db.session.commit()


def store_players(players):
    for player in players:
        db.session.add(player)
    db.session.commit()


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
