from app import db
from app.skill.model import SkillHistory


def get_history_for_player(id, pagination):
    history = (SkillHistory.query.filter(SkillHistory.player_id == id)
                                 .paginate(pagination.page,
                                           pagination.page_size,
                                           False))
    return history


def get_history_for_player_from_date(id, date, pagination):
    history = (SkillHistory.query.filter(SkillHistory.player_id == id,
                                         SkillHistory.date >= date)
                                 .paginate(pagination.page,
                                           pagination.page_size,
                                           False))
    return history


def store_skill_history(skill_history):
    db.session.add(skill_history)


def store_skill_histories(skill_history):
    for skill_history in skill_history:
        db.session.add(SkillHistory)
