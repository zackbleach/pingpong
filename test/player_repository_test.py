import os
import unittest

from config import basedir
from app import app, db
from app.models.player import Player
from app.repository import player_repository


class PlayerRepoTest(unittest.TestCase):

    ID = 10
    NAME = "gfhudgZack"
    EMAIL = "zack@brandwatch.com"
    AVATAR = "gravatar"
    OFFICE = "San Francisco"

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///'
                                                 + os.path.join(basedir,
                                                                'test.db'))
        self.app = app.test_client()
        print app.config['SQLALCHEMY_DATABASE_URI']
        db.create_all()
        db.session.add(self.create_player_for_test())
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_my_first_test(self):
        print app.config['SQLALCHEMY_DATABASE_URI']
        player = player_repository.get_player_by_id(self.ID)
        assert(player.id == self.ID)

    def create_player_for_test(self):
        return Player(id=self.ID,
                      name=self.NAME,
                      email=self.EMAIL,
                      avatar=self.AVATAR,
                      office=self.OFFICE)

if __name__ == '__main__':
    unittest.main()
