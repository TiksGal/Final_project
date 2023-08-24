from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from run import app, db


class Player(db.Model, UserMixin):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column("username", db.String(20), unique=True, nullable=False)
    name = db.Column("name", db.String(60), nullable=False)
    surname = db.Column("surname", db.String(60), nullable=False)
    password = db.Column("password", db.String(60), nullable=False)
    email = db.Column("email", db.String(120), unique=True, index=True, nullable=False)
    games_won = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    games_lost = db.Column(db.Integer, default=0)
    correct_guess = db.Column(db.Integer, default=0)
    wrong_guess = db.Column(db.Integer, default=0)
    tries = db.Column(db.Integer, default=0)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return Player.query.get(user_id)
