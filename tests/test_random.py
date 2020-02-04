import unittest
from app import app, db
from app.models import User, Boardgame


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_randomfunc(self):
        u1 = User(username="john", email="john@example.com")

        game1 = Boardgame(
            title="Kingdomino",
            player_number_min=2,
            player_number_max=4,
            playtime_low=15,
            playtime_max=30,
        )

        game2 = Boardgame(
            title="Aeon's end",
            player_number_min=1,
            player_number_max=4,
            playtime_low=60,
            playtime_max=180,
        )
        
        game3 = Boardgame(
            title="Terraforming Mars",
            player_number_min=1,
            player_number_max=5,
            playtime_low=60,
            playtime_max=999,
        )

        db.session.add(u1)
        db.session.commit()
        result = u1.random_game()
        self.assertIsNone(result) 

        u1.add_game(game1)
        u1.add_game(game2)
        db.session.commit()

        self.assertIsNotNone(u1.random_game())
        self.assertIsNotNone(u1.random_game(player_number_max=4))
        self.assertIsNone(u1.random_game(player_number_max=5))
        self.assertIsNone(u1.random_game(playtime_max=181))