from app.models.participant import Participant
from app import db


def store_participants_from_game(game):
    for participant in game.winners + game.losers:
        new_participant = Participant(player_id=participant.id,
                                      game_id=game.id,
                                      winner=(participant in game.winners)
                                      )
        db.session.add(new_participant)
