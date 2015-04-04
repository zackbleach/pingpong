from app.repository.game_repository import get_game_by_id


def game_exists(id):
    game = get_game_by_id(id)
    return game is not None
