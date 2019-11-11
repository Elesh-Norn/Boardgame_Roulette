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


    def test_collection(self):
        u1 = User(username="john", email="john@example.com")
        u2 = User(username="susan", email="susan@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.collection.all(), [])
        self.assertEqual(u1.collection.all(), [])

        game1 = Boardgame(title = "Kingdomino",
                          player_number_min=2,
                          player_number_max=4,
                          playtime_low=15,
                          playtime_max=30)

        game2 = Boardgame(title="Aeon's end",
                          player_number_min=1,
                          player_number_max=4,
                          playtime_low=60,
                          playtime_max=180)

        game3 = Boardgame(title="Terraforming Mars",
                          player_number_min=1,
                          player_number_max=5,
                          playtime_low=60,
                          playtime_max=999)

        u1.add_game(game1)
        db.session.commit()
        self.assertEqual(u1.collection.first().title, "Kingdomino")

        u2.add_game(game2)
        db.session.commit()
        self.assertEqual(u2.collection.first().title, "Aeon's end")

        u1.add_game(game3)
        u2.add_game(game3)
        db.session.commit()
        titles_1 = [x.title for x in u1.collection]
        titles_2 = [x.title for x in u2.collection]

        self.assertTrue('Kingdomino' in titles_1)
        self.assertFalse("Aeon's end" in titles_1)

        self.assertTrue("Aeon's end" in titles_2)
        self.assertFalse("Kingdomino" in titles_2)

        self.assertTrue("Terraforming Mars" in titles_1)
        self.assertTrue("Terraforming Mars" in titles_2)

        self.assertTrue(u1.own_game(game1))
        self.assertFalse(u1.own_game(game2))
        self.assertTrue(u1.own_game(game3))


if __name__ == "__main__":
    unittest.main(verbosity=2)
