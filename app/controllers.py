from app import app
from flask import request
from models import Participant
from models import Player
from models import Game
from flask import jsonify
from app import db
from trueskill import Rating, rate_1vs1, quality_1vs1
import json
from config import api_path

game_api_path = api_path+'/'+Game.collection_name


@app.route(game_api_path, methods=['POST'])
def store_game():
    game = json.loads(request.data)
    my_loser_score = game.get('loser_score')
    new_game = Game(loser_score=my_loser_score)
    db.session.add(new_game)
    db.session.commit()

    winner = game.get('winner')[0]
    loser = game.get('loser')[0]

    store_participants_from_game(winner, loser, new_game)
    update_skill(winner, loser)
    return jsonify(game=new_game.to_json())


def update_skill(winner, loser):
    winning_player = Player.query.filter_by(id=winner.get('id')).first()
    losing_player = Player.query.filter_by(id=loser.get('id')).first()

    winning_previous_rating = Rating(winning_player.skill,
                                     winning_player.skill_sd)
    loser_previous_rating = Rating(losing_player.skill,
                                   winning_player.skill_sd)

    winning_new_rating, loser_new_rating = rate_1vs1(winning_previous_rating,
                                                     loser_previous_rating)
    winning_player.skill = winning_new_rating.mu
    losing_player.skill = loser_new_rating.mu

    winning_player.skill_sd = winning_new_rating.sigma
    losing_player.skill_sd = loser_new_rating.sigma

    db.session.add(winning_player)
    db.session.add(losing_player)
    db.session.commit()


def store_participants_from_game(winner, loser, game):
    winning_participant = Participant(player_id=winner.get('id'),
                                      game_id=game.id, winner=True)
    db.session.add(winning_participant)

    losing_participant = Participant(player_id=loser.get('id'),
                                     game_id=game.id, winner=False)
    db.session.add(losing_participant)
    db.session.commit()


@app.route(api_path+'/'+'draw'+'/<player_one>/<player_two>', methods=['GET'])
def quality(player_one, player_two):

    player_one = Player.query.filter_by(id=player_one).first()
    player_two = Player.query.filter_by(id=player_two).first()

    player_one_ranking = Rating(player_one.skill, player_one.skill_sd)
    player_two_ranking = Rating(player_two.skill, player_two.skill_sd)

    quality = quality_1vs1(player_one_ranking, player_two_ranking)
    chance_of_draw = '{:.1%}'.format(quality)

    return jsonify(chance_of_draw=chance_of_draw)
