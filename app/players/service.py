from app.players.repository import (store_player,
                                    get_player_by_id,
                                    get_player_by_email)
from trueskill import rate, quality_1vs1


def get_chance_of_draw(player_one_id, player_two_id):
    player_one = get_player_by_id(player_one_id)
    player_two = get_player_by_id(player_two_id)
    quality = quality_1vs1(player_one.get_rating(), player_two.get_rating())
    return quality


def update_players_skill_from_game(game):
    winner_ratings = {winner: winner.get_rating() for winner in game.winners}
    loser_ratings = {loser: loser.get_rating() for loser in game.losers}

    new_ratings = rate([winner_ratings, loser_ratings], ranks=[0, 1])

    for group in new_ratings:
        for player in group.keys():
            player.skill = group[player].mu
            player.skill_sd = group[player].sigma
            store_player(player)


def player_exists(id):
    try:
        player = get_player_by_id(id)
    except ValueError:
        return False
    return player is not None


def player_exists_by_email(email):
    try:
        player = get_player_by_email(email)
    except ValueError:
        return False
    return player is not None
