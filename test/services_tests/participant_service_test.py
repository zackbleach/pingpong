from app.models.game import Game
from app.models.player import Player
from nose.tools import assert_equals
from mock import Mock


class TestParticipantService():

    PLAYER_ID = 1
    PLAYER_FIRST_NAME = "Zack"
    PLAYER_LAST_NAME = "Bleach"
    PLAYER_EMAIL = "zack@brandwatch.com"
    PLAYER_AVATAR = "http://zackblea.ch"
    PLAYER_OFFICE = "San Francisco"

    GAME_ID = 1
    GAME_LOSER_SCORE = 15

    def setup(self):
        pass

    def teardown(self):
        pass

    def mock_me(self):
        return 2

    def create_player(self):
        return Player(id=self.PLAYER_ID,
                      first_name=self.PLAYER_FIRST_NAME,
                      last_name=self.PLAYER_LAST_NAME,
                      email=self.PLAYER_EMAIL,
                      avatar=self.PLAYER_AVATAR,
                      office=self.PLAYER_OFFICE)

    def create_game(self):
        player_one = self.create_player()
        player_two = self.create_player()
        return Game(id=self.ID,
                    loser_score=self.LOSER_SCORE,
                    winners=[player_one],
                    losers=[player_two])
