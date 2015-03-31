from app import db
from trueskill import Rating


class Player(db.Model):
    collection_name = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    avatar = db.Column(db.String(120), nullable=False)
    skill = db.Column(db.Float, default=25)
    skill_sd = db.Column(db.Float, default=8.333333333333334)
    office = db.Column(db.Enum('San Francisco',
                               'Brighton',
                               'Berlin',
                               'New York',
                               'Stuttgart'), nullable=False)

    def to_json(self):
        return dict(id=self.id,
                    name=self.name,
                    email=self.email,
                    avatar=self.avatar,
                    skill=self.skill,
                    skill_sd=self.skill_sd,
                    office=self.office
                    )

    def get_rating(self):
        return Rating(self.skill, self.skill_sd)

    def __repr__(self):
            return '<User %r>' % (self.name)
