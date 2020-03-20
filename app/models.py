from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy import func
from time import time
import jwt
from app import app


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)

boardgames = db.Table(
    "boardgames",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("boardgame_id", db.Integer, db.ForeignKey("boardgame.id")),
)


class Boardgame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    player_number_min = db.Column(db.Integer)
    player_number_max = db.Column(db.Integer)
    playtime_low = db.Column(db.Integer)
    playtime_max = db.Column(db.Integer)
    genre = db.Column(db.String(140))
    difficulty = db.Column(db.String(140))

    def __repr__(self):
        return "<Boardgame {}>".format(self.title)


class SearchFilters:

    def search_player_count(game_list, value):
        return game_list.filter(
            Boardgame.player_number_max >= value
            ).filter(Boardgame.player_number_min <= value)
    def search_play_time(game_list, value):
        return game_list.filter(
            Boardgame.playtime_max >= value
            ).filter(Boardgame.playtime_low <= value)
    def search_genre(game_list, value):
        return game_list.filter(Boardgame.genre == value)

    def search_difficulty(game_list, value):
        return game_list.filter(Boardgame.difficulty == value)


filters = {
    "player": SearchFilters.search_player_count, 
    "time": SearchFilters.search_play_time,
    "genre": SearchFilters.search_genre,
    "difficulty": SearchFilters.search_difficulty
           }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    collection = db.relationship("Boardgame", secondary=boardgames, lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def add_game(self, game):
        self.collection.append(game)

    def own_game(self, game):
        return self.collection.filter(boardgames.c.boardgame_id == game.id).count() > 0

    # TODO remove game from collection

    def random_game(self, result):
        game_list = self.collection
        for key, value in result.items():
            if key in filters:
                game_list = filters[key](game_list, value)
        return game_list.order_by(func.random()).first()

    def __repr__(self):
        return "<User {}>".format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size
        )

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password.txt": self.id, "exp": time() + expires_in},
            app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])[
                "reset_password.txt"
            ]
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)