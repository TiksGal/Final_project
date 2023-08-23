from os import path
from flask import session, flash, redirect, url_for
from app.db_crud import DbCrud
import logging
import logging.config
import random


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

WORDFILE = "./app/dictionary/countries.txt"

db_crud = DbCrud()

class Functions():
    pass
    @staticmethod
    def get_random_word():
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
                
    # Check if a user is authenticated
    def is_authenticated(self):
        if 'player_name' not in session:
            flash("Please log in to play!", "warning")
            return False
        player = db_crud.get_player_by_username(session["player_name"])
        if not player:
            flash("Player session expired. Please login again.", "danger")
            return False
        return player

    # Initialize game session if required
    def init_game_session(self):
        session.setdefault('usable_letters', "abcdefghijklmnopqrstuvwxyz")
        session.setdefault('wrong_letters', [])
        session.setdefault('tries', 10)
        session.setdefault('word_to_guess', Functions.get_random_word())
        session.setdefault('visuals', ['_' if ch != ' ' else ' ' for ch in session['word_to_guess']])


    def handle_guess(self, player, guess):
        # Normalize guess
        guess = guess.lower().strip()

        # Invalid guess checks
        if (not guess.isalpha()) or \
        (len(guess) == 1 and guess not in session['usable_letters']) or \
        (len(guess) > 1 and guess != session['word_to_guess']):
            session['tries'] -= 1
            flash("Invalid guess. Please use the provided letters or guess the word.", "danger")
            
            # Check if the game has ended due to invalid guess
            if session['tries'] == 0:
                self.end_game(player, False)
                return redirect(url_for('game_lost'))
            
            return None

        # Valid word guess
        if len(guess) > 1 and guess == session['word_to_guess']:
            self.end_game(player, True)
            return redirect(url_for('game_won'))

        # Incorrect word guess
        if len(guess) > 1:
            session['tries'] -= 1
            if session['tries'] == 0:
                self.end_game(player, False)
                return redirect(url_for('game_lost'))
            flash("Your word guess was incorrect!", "warning")
            return None

        # Valid letter guess
        session['usable_letters'] = session['usable_letters'].replace(guess, "")
        if guess in session['word_to_guess']:
            for idx, char in enumerate(session['word_to_guess']):
                if char == guess:
                    session['visuals'][idx] = guess
        else:  # Wrong letter guess
            session['wrong_letters'].append(guess)
            session['tries'] -= 1

        # Game termination checks
        if session['tries'] == 0:
            self.end_game(player, False)
            return redirect(url_for('game_lost'))
        elif "_" not in session['visuals']:
            self.end_game(player, True)
            return redirect(url_for('game_won'))
        
        return None


    def end_game(self, player, won):
        correct_guesses = len([ch for ch in session['visuals'] if ch != '_'])
        wrong_guesses = len(session['wrong_letters'])

        if won:
            db_crud.update_player_after_won_game(player, correct_guesses, wrong_guesses)
            flash(f"Congratulations! You've guessed the word: {session['word_to_guess']}", "success")
        else:
            db_crud.update_player_after_lost_game(player, correct_guesses, wrong_guesses)
            flash(f"Secret word was - {session['word_to_guess']}", "danger")

        keys_to_remove = ['usable_letters', 'wrong_letters', 'tries', 'word_to_guess', 'visuals']
        for key in keys_to_remove:
            session.pop(key)

    