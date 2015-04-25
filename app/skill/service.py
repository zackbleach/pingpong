from app.skill.model import SkillHistory
from app.skill.repository import store_skill_history
from datetime import datetime


def store_skill_histories_from_game(game):
    for player in game.get_players():
        store_skill_history_for_player(player)


def store_skill_history_for_player(player):
    history = SkillHistory(player_id=player.id,
                           skill=player.skill,
                           skill_sd=player.skill_sd,
                           date=datetime.utcnow())
    store_skill_history(history)
