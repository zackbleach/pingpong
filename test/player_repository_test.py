import os

from config import basedir
from app import app, db
from app.models.player import Player
from nose.tools import raises, assert_equals
from sqlalchemy.exc import IntegrityError


class TestPlayerRepo():

    ID = 10
    FIRST_NAME = "Zack"
    LAST_NAME = "Bleach"
    EMAIL = "zack@brandwatch.com"
    AVATAR = "gravatar"
    OFFICE = "San Francisco"

    def setup(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'
                                                 + os.path.join(basedir,
                                                                'test.db'))
        self.app = app.test_client()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    # def store_and_retrieve_player_test(self):
    #     db.session.add(self.create_player())
    #     db.session.flush()
    #     player = Player.query.filter_by(id=self.ID).first()
    #     assert_equals(player.id, self.create_player().id)

    # @raises(IntegrityError)
    # def store_duplicate_player_test(self):
    #     db.session.add(self.create_player())
    #     db.session.add(self.create_player())
    #     db.session.commit()

    def create_player(self):
        return Player(id=self.ID,
                      first_name=self.FIRST_NAME,
                      last_name=self.LAST_NAME,
                      email=self.EMAIL,
                      avatar=self.AVATAR,
                      office=self.OFFICE)
