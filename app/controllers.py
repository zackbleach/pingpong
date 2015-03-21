import json
from app import app
from app import db
from config import API_PATH
from flask import jsonify
from flask import request
from models import Game
from models import Participant
from models import Player
from trueskill import Rating, rate, quality_1vs1

GAME_API_PATH = API_PATH + '/' + Game.collection_name


@app.route(GAME_API_PATH, methods=['POST'])
def store_game():
    game = json.loads(request.data)
    my_loser_score = game.get('loser_score')
    new_game = Game(loser_score=my_loser_score)
    db.session.add(new_game)
    db.session.commit()

    winners = game.get('winners')
    losers = game.get('losers')

    store_participants_from_game(winners, losers, new_game)
    update_skill(winners, losers)
    return jsonify(game=new_game.to_json())


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


def store_participants_from_game(winners, losers, game):
    for winner in winners:
        winning_participant = Participant(player_id=winner.get('id'),
                                          game_id=game.id, winner=True)
        db.session.add(winning_participant)

    for loser in losers:
        losing_participant = Participant(player_id=loser.get('id'),
                                         game_id=game.id, winner=False)
        db.session.add(losing_participant)

    db.session.commit()


@app.route(API_PATH+'/'+'draw'+'/<player_one>/<player_two>', methods=['GET'])
def quality(player_one, player_two):

    player_one = Player.query.filter_by(id=player_one).first()
    player_two = Player.query.filter_by(id=player_two).first()

    player_one_ranking = Rating(player_one.skill, player_one.skill_sd)
    player_two_ranking = Rating(player_two.skill, player_two.skill_sd)

    quality = quality_1vs1(player_one_ranking, player_two_ranking)
    chance_of_draw = '{:.1%}'.format(quality)

    return jsonify(chance_of_draw=chance_of_draw)
