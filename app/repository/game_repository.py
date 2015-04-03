from app import app, db
from app.models.participant import Participant
from app.models.game import Game
from sqlalchemy import desc


def get_games_for_player(player_id):
    games = (db.session.query(Game)
               .join(Participant)
               .filter(Participant.player_id == player_id)
               .order_by(desc(Game.id))
               .all())
    return games
