from app import db
from app.models.player import Player


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
