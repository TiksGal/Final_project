from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, login_required, logout_user
from app.models.models import Player
from app import app, db, bcrypt
from app.functions import Functions
from app.db_crud import DbCrud
from app.forms.forms import LoginForm, RegistrationForm


functions = Functions()
db_crud = DbCrud()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated and 'player_name' in session:
        return redirect(url_for("game_route"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_crud.get_player_by_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session['player_name'] = user.username  # Setting 'player_name' in session
            return redirect(url_for("start_game"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("home"))

@app.route('/start_game', methods=['GET', 'POST'])
@login_required
def start_game():
    if request.method == 'POST':
        return redirect(url_for("game_route"))
    return render_template('start_game.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = db_crud.get_player_by_username(form.username.data)
        if user:  
            flash("Username already exists! Please choose another username.")
            login_user(new_user)
            session['player_name'] = new_user.username
            return render_template("register.html", title="Register", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = db_crud.create_player(username=form.username.data, 
                                         name=form.name.data,
                                         surname=form.surname.data,
                                         hashed_password=hashed_password,
                                         email=form.email.data)
        if not new_user:
            flash("Error creating new player!")
            return render_template("register.html", title="Register", form=form)
        flash("Registration successful! Please log in.")
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)


def clear_game_data_from_session():
    keys_to_remove = ['usable_letters', 'wrong_letters', 'tries', 'word_to_guess', 'visuals']
    for key in keys_to_remove:
        session.pop(key, None)

@app.route('/game', methods=['GET', 'POST'])
def game_route():
    if 'player_name' not in session:
        flash("Please log in to play!", "warning")
        return redirect(url_for('login'))

    player = db_crud.get_player_by_username(session["player_name"])
    if not player:
        flash("Player session expired. Please login again.", "danger")
        return redirect(url_for('login'))

    # Initialize session variables
    session.setdefault('usable_letters', "abcdefghijklmnopqrstuvwxyz")
    session.setdefault('wrong_letters', [])
    session.setdefault('tries', 10)
    session.setdefault('word_to_guess', functions.get_random_word())
    session.setdefault('visuals', ['_' if ch != ' ' else ' ' for ch in session['word_to_guess']])

    if request.method == 'POST':
        player.games_played += 1
        db.session.commit()

    hangman_image = functions.get_image(tries=session['tries']) # Assuming you use this image in the template

    return render_template('game.html', tries=session['tries'], visuals=session['visuals'], usable_letters=session['usable_letters'], player=player, hangman_image=hangman_image)

@app.route('/add_char', methods=["POST"])
def add_char():
    if 'player_name' not in session:
        flash("Please log in to play!", "warning")
        return redirect(url_for('login'))

    player = db_crud.get_player_by_username(session["player_name"])
    if not player:
        flash("Player session expired. Please login again.", "danger")
        return redirect(url_for('login'))

    guess = request.form["guess"]
    session['usable_letters'] = session['usable_letters'].replace(guess, "")

    if guess in session['word_to_guess']:
        for idx, char in enumerate(session['word_to_guess']):
            if char == guess:
                session['visuals'][idx] = guess
    else:
        session['wrong_letters'].append(guess)
        session['tries'] -= 1

    if session['tries'] == 0:
        correct_guesses = len([ch for ch in session['visuals'] if ch != '_'])
        wrong_guesses = len(session['wrong_letters'])
        db_crud.update_player_after_lost_game(player, correct_guesses, wrong_guesses)
        flash(f"Secret word was - {session['word_to_guess']}", "danger")
        clear_game_data_from_session()
        return redirect(url_for('game_lost'))
    elif "_" not in session['visuals']:
        correct_guesses = len(session['visuals'])
        wrong_guesses = len(session['wrong_letters'])
        db_crud.update_player_after_won_game(player, correct_guesses, wrong_guesses)
        flash(f"Congratulations! You've guessed the word: {session['word_to_guess']}", "success")
        clear_game_data_from_session()
        return redirect(url_for('game_won'))
    hangman_image = functions.get_image(tries=session['tries']) # Assuming you use this image in the template

    return render_template('game.html', tries=session['tries'], visuals=session['visuals'], usable_letters=session['usable_letters'], player=player, hangman_image=hangman_image)


@app.route('/scoreboard')
def scoreboard():
    players = db_crud.get_all_players()
    players_data = db_crud.get_players_game_data(players)
    sorted_players = sorted(players_data, key=lambda x: x['games_won'], reverse=True)
    return render_template('scoreboard.html', players=sorted_players)

@app.route('/game_lost')
def game_lost():
    return render_template('game_lost.html')

@app.route('/game_won', methods=['GET'])
def game_won():
    return render_template('game_won.html')



