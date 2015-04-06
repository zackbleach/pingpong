import os

from config import basedir
from app import app, db
from app.models.player import Player
from nose.tools import raises, assert_equals
from sqlalchemy.exc import IntegrityError


class TestPlayerRepo():

    ID = 1
    FIRST_NAME = "Zack"
    LAST_NAME = "Bleach"
    EMAIL = "zack@brandwatch.com"
    AVATAR = "http://zackblea.ch"
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

    def store_and_retrieve_player_test(self):
        db.session.add(self.create_player())
        player = Player.query.filter_by(id=self.ID).first()
        assert_equals(player.id, self.create_player().id)

    # @raises(IntegrityError)
    # def store_player_with_no_first_name_test(self):
    #     player = self.create_player()
    #     player.first_name = None
    #     db.session.add(player)
    #     db.session.commit()

    # @raises(IntegrityError)
    # def store_player_with_no_avatar_test(self):
    #     player = self.create_player()
    #     player.avatar = None
    #     db.session.add(player)
    #     db.session.commit()

    # @raises(IntegrityError)
    # def store_player_with_no_office_test(self):
    #     player = self.create_player()
    #     player.office = None
    #     db.session.add(player)
    #     db.session.commit()

    # @raises(IntegrityError)
    # def store_player_with_invalid_office_test(self):
    #     player = self.create_player()
    #     player.office = "Birmingham"
    #     db.session.add(player)
    #     db.session.commit()

    # @raises(IntegrityError)
    # def store_player_with_no_email_test(self):
    #     player = self.create_player()
    #     player.email = ""
    #     db.session.add(player)
    #     db.session.commit()

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
