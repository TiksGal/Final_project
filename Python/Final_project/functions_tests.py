import unittest
from flask import session
from app import app
from app.functions import Functions


class TestFunctions(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        self.request_context = app.test_request_context()
        self.request_context.push()
        self.functions = Functions()

    def tearDown(self):
        self.request_context.pop()  # Pop the request context
        self.app_context.pop()

    def test_get_random_word(self):
        word = self.functions.get_random_word()
        self.assertIsNotNone(word)
        self.assertTrue(word.isalpha())

    def test_create_game_gui(self):
        gui = self.functions.create_game_gui(5)
        self.assertEqual(gui, ["_", "_", "_", "_", "_"])

        gui = self.functions.create_game_gui(0)
        self.assertEqual(gui, [])

    def test_get_image(self):
        for i in range(0, 10):
            image_path = self.functions.get_image(i)
            self.assertEqual(image_path, f"./app/static/images/{i}.png")

    def test_is_authenticated(self):
        result = self.functions.is_authenticated()
        # Assuming no player is authenticated at the start
        self.assertFalse(result)

    # Assuming this test is run after the above one
    def test_init_game_session(self):
        self.functions.init_game_session()

        self.assertIn("usable_letters", session)
        self.assertIn("wrong_letters", session)
        self.assertIn("tries", session)
        self.assertIn("word_to_guess", session)
        self.assertIn("visuals", session)

        self.assertEqual(session["tries"], 10)
        self.assertEqual(session["usable_letters"], "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(len(session["word_to_guess"]), len(session["visuals"]))


if __name__ == "__main__":
    unittest.main()
