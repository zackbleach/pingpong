from trueskill import rate, quality_1vs1
from app.repository.player_repository import store_player


def update_players_skill_from_game(game):
    winner_ratings = {winner: winner.get_rating() for winner in game.winners}
    loser_ratings = {loser: loser.get_rating() for loser in game.losers}

    new_ratings = rate([winner_ratings, loser_ratings], ranks=[0, 1])

    for group in new_ratings:
        for player in group.keys():
            player.skill = group[player].mu
            player.skill_sd = group[player].sigma
        store_player(player)


def get_chance_of_draw(player_one, player_two):
    quality = quality_1vs1(player_one.get_rating(), player_two.get_rating())
    chance_of_draw = '{:.1%}'.format(quality)
    return chance_of_draw
