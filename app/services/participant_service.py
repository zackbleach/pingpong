from app.models.participant import Participant
from app.repository.participant_repository import store_participant


def store_participants_from_game(game):
    for participant in game.winners + game.losers:
        new_participant = Participant(player_id=participant.id,
                                      game_id=game.id,
                                      winner=(participant in game.winners)
                                      )
        store_participant(new_participant)
