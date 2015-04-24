from app import db


def store_participant(participant):
    db.session.add(participant)
