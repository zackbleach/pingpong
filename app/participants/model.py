from app import db


class Participant(db.Model):
    collection_name = 'participants'
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'),
                          primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    winner = db.Column(db.Boolean)

    def __repr__(self):
        return '<Participant: Player = %r, Game = %r>' % (self.player_id,
                                                          self.game_id)
