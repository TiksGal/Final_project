from os import path
import logging
import logging.config
import random


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

WORDFILE = "./app/dictionary/countries.txt"


class Functions():
    pass

    def get_random_word(self):
        """Get a random word from the wordlist using no extra memory."""
        num_words_processed = 0
        curr_word = None
        with open(WORDFILE, 'r') as f:
            for word in f:
                word = word.strip().lower()
                num_words_processed += 1
                if random.randint(1, num_words_processed) == 1:
                    curr_word = word
        return curr_word


    def create_game_gui(self, lenght: int) -> str:
            try:
                view = ["_" for _ in range(0, lenght)]
                return view
            except Exception as e:
                logger.error(e)

                
    def get_image(self, tries: int) -> str:
            try:
                return f"./app/static/images/{tries}.png"
            except Exception as e:
                logger.error(e)
