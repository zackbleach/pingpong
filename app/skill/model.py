from app import db
from datetime import datetime


class SkillHistory(db.Model):
    collection_name = 'skill_history'
    id = db.Column(db.Integer, nullable=False, unique=True,
                   autoincrement=True, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    skill = db.Column(db.Float, default=25)
    skill_sd = db.Column(db.Float, default=8.333333333333334)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return ('<Skill History: Player = %r, \
                Skill = %r, Date = %r>' % (self.player_id,
                                           self.skill,
                                           self.date))

    def to_json(self):
        return dict(player_id=self.player_id,
                    skill=self.skill,
                    skill_sd=self.skill_sd,
                    date=self.date)
