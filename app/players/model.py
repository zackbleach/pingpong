import re
from app import db
from config import Config
from validate_email import validate_email
from sqlalchemy.orm import validates
from trueskill import Rating

class Player(db.Model):

    collection_name = 'players'
    id = db.Column(db.Integer, primary_key=True, index=True,
                   autoincrement=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    nick_name = db.Column(db.String(32))
    email = db.Column(db.String(120),
                      index=True,
                      unique=True,
                      nullable=False)
    avatar = db.Column(db.String(120), nullable=False)
    skill = db.Column(db.Float, default=25)
    skill_sd = db.Column(db.Float, default=8.333333333333334)
    office = db.Column(db.Enum(*Config.OFFICES), nullable=False)
    google_id = db.Column(db.Text())

    def to_json(self):
        return dict(id=self.id,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    nick_name=self.nick_name,
                    email=self.email,
                    avatar=self.avatar,
                    skill=self.skill,
                    skill_sd=self.skill_sd,
                    office=self.office,
                    google_id=self.google_id
                    )

    def get_rating(self):
        return Rating(self.skill, self.skill_sd)

    def __repr__(self):
        return '<User: id = %r, name = %r %r>' % (self.id,
                                                  self.first_name,
                                                  self.last_name)

    # @validates('email')
    def check_email(self, key, email):
        valid_email = validate_email(email)
        if not valid_email:
            raise ValueError('Email not valid: %s' % email)
        return email

    @validates('first_name')
    @validates('last_name')
    @validates('avatar')
    def validate_name(self, key, name):
        message = 'Property \'%s\' must be shorter than 64 characters'
        if name is None or len(name) > 64:
            raise ValueError(message % key)
        return name

    @validates('avatar')
    def validate_avatar_url(self, key, url):
        message = 'Avatar URL not valid: %s'
        # Django URL Validation Regex. Why isn't there a library for this?
        url_regex = re.compile(
            r'^(?:http)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if url is None or not url_regex.match(url):
            raise ValueError(message % url)
        return url

    @validates('office')
    def valid_offices(self, key, office):
        valid_offices = ('Brighton',
                         'New York',
                         'Berlin',
                         'San Francisco',
                         'Stuttgart',
                         'London',
                         '')
        if office is None or office not in valid_offices:
            raise ValueError('Office: %s is not recognised.' % office)
        return office
