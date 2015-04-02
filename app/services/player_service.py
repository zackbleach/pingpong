from app.models.player import Player
from app.repository.player_repository import get_player_by_id, store_player
from sqlalchemy import and_, desc
from trueskill import rate, quality_1vs1


def get_chance_of_draw(player_one, player_two):
    quality = quality_1vs1(player_one.get_rating(), player_two.get_rating())
    chance_of_draw = '{:.1%}'.format(quality)
    return chance_of_draw


def update_players_skill_from_game(game):
    winner_ratings = {winner: winner.get_rating() for winner in game.winners}
    loser_ratings = {loser: loser.get_rating() for loser in game.losers}

    new_ratings = rate([winner_ratings, loser_ratings], ranks=[0, 1])

    for group in new_ratings:
        for player in group.keys():
            player.skill = group[player].mu
            player.skill_sd = group[player].sigma
        store_player(player)


def get_players_above(player_id, number_of_players):
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


def get_players_below(player_id, number_of_players):
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
