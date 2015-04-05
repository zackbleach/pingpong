from app import db
from app.models.skill_history import SkillHistory


def get_history_for_player(id):
    history = SkillHistory.query.filter(SkillHistory.player_id == id).all()
    return history


def store_skill_history(skill_history):
    db.session.add(skill_history)


def store_skill_histories(skill_history):
    for skill_history in skill_history:
        db.session.add(SkillHistory)
