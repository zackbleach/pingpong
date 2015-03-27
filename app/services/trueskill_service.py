from models import Player
from trueskill import Rating, rate, quality_1vs1
from app import db


def update_skill(winners, losers):

    winners_old_ratings = {}
    losers_old_ratings = {}

    for winner in winners:
        winning_player = Player.query.filter_by(id=winner.get('id')).first()
        winners_old_ratings[winning_player] = Rating(winning_player.skill,
                                                     winning_player.skill_sd)

    for loser in losers:
        losing_player = Player.query.filter_by(id=loser.get('id')).first()
        losers_old_ratings[losing_player] = Rating(losing_player.skill,
                                                   winning_player.skill_sd)

    winner_new_ratings, loser_new_ratings = rate([winners_old_ratings,
                                                 losers_old_ratings],
                                                 ranks=[0, 1])

    for winner in winner_new_ratings.keys():
        winner.skill = winner_new_ratings[winner].mu
        winner.skill_sd = winner_new_ratings[winner].sigma
        db.session.add(winner)

    for loser in loser_new_ratings.keys():
        loser.skill = loser_new_ratings[loser].mu
        loser.skill_sd = loser_new_ratings[loser].sigma
        db.session.add(loser)

    db.session.commit()


def quality(player_one, player_two):

    player_one = Player.query.filter_by(id=player_one).first()
    player_two = Player.query.filter_by(id=player_two).first()

    player_one_ranking = Rating(player_one.skill, player_one.skill_sd)
    player_two_ranking = Rating(player_two.skill, player_two.skill_sd)

    quality = quality_1vs1(player_one_ranking, player_two_ranking)
    chance_of_draw = '{:.1%}'.format(quality)

    return jsonify(chance_of_draw=chance_of_draw)

