from app.participants.model import Participant
from app.participants.repository import store_participant


def store_participants_from_game(game):
    for participant in game.winners + game.losers:
        new_participant = Participant(player_id=participant.id,
                                      game_id=game.id,
                                      winner=(participant in game.winners)
                                      )
        store_participant(new_participant)
