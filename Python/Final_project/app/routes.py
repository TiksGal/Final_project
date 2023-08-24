from flask import render_template, redirect, url_for, flash, session, request
from flask_login import current_user, login_user, login_required, logout_user
from app.models.models import Player
from app import app, db, bcrypt
from app.functions import Functions
from app.db_crud import DbCrud
from app.forms.forms import LoginForm, RegistrationForm


functions = Functions()
db_crud = DbCrud()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user and current_user.is_authenticated and "player_name" in session:
        return redirect(url_for("game_route"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db_crud.get_player_by_username(form.username.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            session["player_name"] = user.username  # Setting 'player_name' in session
            return redirect(url_for("start_game"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("home"))


@app.route("/start_game", methods=["GET", "POST"])
@login_required
def start_game():
    if request.method == "POST":
        return redirect(url_for("game_route"))
    return render_template("start_game.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = db_crud.get_player_by_username(form.username.data)
        if new_user:
            flash("Username already exists! Please choose another username.")
            login_user(new_user)
            session["player_name"] = new_user.username
            return render_template("register.html", title="Register", form=form)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = db_crud.create_player(
            username=form.username.data,
            name=form.name.data,
            surname=form.surname.data,
            hashed_password=hashed_password,
            email=form.email.data,
        )
        if not new_user:
            flash("Error creating new player!")
            return render_template("register.html", title="Register", form=form)
        flash("Registration successful! Please log in.")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/game", methods=["GET", "POST"])
def game_route():
    player = functions.is_authenticated()
    if not player:
        return redirect(url_for("login"))

    functions.init_game_session()

    if request.method == "POST":
        player.games_played += 1
        db.session.commit()

    hangman_image = functions.get_image(tries=session["tries"])
    return render_template(
        "game.html",
        tries=session["tries"],
        visuals=session["visuals"],
        usable_letters=session["usable_letters"],
        player=player,
        hangman_image=hangman_image,
        wrong_letters=session["wrong_letters"],
    )


@app.route("/add_char", methods=["POST"])
def add_char():
    player = functions.is_authenticated()
    if not player:
        return redirect(url_for("login"))

    guess = request.form["guess"]
    game_end_response = functions.handle_guess(
        player, guess.strip().lower()
    )  # Ensure guesses are cleaned and standardized
    if game_end_response:  # If the game has ended
        return game_end_response

    hangman_image = functions.get_image(tries=session["tries"])
    return render_template(
        "game.html",
        tries=session["tries"],
        visuals=session["visuals"],
        usable_letters=session["usable_letters"],
        player=player,
        hangman_image=hangman_image,
        wrong_letters=session["wrong_letters"],
    )


@app.route("/scoreboard")
def scoreboard():
    players = db_crud.get_all_players()
    players_data = db_crud.get_players_game_data(players)
    sorted_players = sorted(players_data, key=lambda x: x["games_won"], reverse=True)
    return render_template("scoreboard.html", players=sorted_players)


@app.route("/game_lost")
def game_lost():
    return render_template("game_lost.html")


@app.route("/game_won", methods=["GET"])
def game_won():
    return render_template("game_won.html")


@app.errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500
