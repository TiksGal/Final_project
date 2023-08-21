from os import path
import logging
import logging.config
from typing import List, Dict
from sqlalchemy.exc import SQLAlchemyError

from app import db
from app.models.models import Player


log_file_path = path.join(path.dirname(path.abspath(__file__)), "logging.conf")
logging.config.fileConfig(log_file_path)
logger = logging.getLogger("sLogger")

class DbCrud:
    pass

    def get_player(self, id: int) -> Player:
        try:
            player = Player.query.get(id)
            if player:
                logger.info(f"'{player.username}' player have been returned successfully!")
                return player
            else:
                logger.error(
                    f"Player with '{id}', does not exist"
                )
                return None
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"An error: '{error}' occured while trying to get player!")


    def get_all_players(self) -> List[Player]:
        try:
            players = Player.query.all()
            logger.info("players have been returned!")
            return players
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"An error: '{error}' occured while getting all players!")


    def create_player(
        self, username: str, name: str, surname: str, hashed_password: str, email: str
    ) -> Player:
        try:
            player = Player(
            username=username,
            name=name,
            surname=surname,
            password=hashed_password,
            email=email,
            )

            db.session.add(player)
            db.session.commit()
            logger.info(f"'{player.username}' player have been created successfully!")
            return player
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"An error: '{error}' occured while creating player!")
            print(f"An error occurred while creating player: {error}")



    def get_players_game_data(self, players: List[Player]) -> List[Dict[str, int]]:
        try:
            players_data = [
                {
                    "username": player.username,
                    "games_won": player.games_won,
                    "games_played": player.games_played,
                    "games_lost": player.games_lost,
                }
                for player in players
            ]
            logger.info(" Players game data have been returned successfully!")
            return players_data
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"An error: '{error}' occured while trying to get players data!")


    def get_player_by_username(self, username: str) -> Player:
        try:
            player = Player.query.filter_by(username=username).first()
            if player:
                logger.info(f"'{player.username}' player have been returned successfully!")
                return player
            else:
                logger.error(
                    f"Player with: '{username}', does not exist!"
                )
                return None
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            logger.error(f"An error: '{error}' occured while trying to get player!")


    def update_player_after_lost_game(
        self, player: Player, correct: int, wrong: int
    ) -> bool:
        try:
            player.games_played += 1
            player.games_lost += 1
            player.wrong_guess += wrong
            player.correct_guess += correct
            db.session.add(player)
            db.session.commit()
            logger.info(f"'{player.username}' updated!")
            
            # Fetch the player again to check
            check_player = Player.query.get(player.id)
            logger.info(f"After update, {check_player.username}'s games_won is {check_player.games_lost} and games_played is {check_player.games_played}")
            return True
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback any changes if an error occurs
            logger.exception(f"An error occurred while updating player '{player.username}'!")
            return False
        finally:
            db.session.close()


    def update_player_after_won_game(
        self, player: Player, correct: int, wrong: int
    ) -> bool:
        try:
            player.games_played += 1
            player.games_won += 1
            player.correct_guess += correct
            player.wrong_guess += wrong
            db.session.add(player)
            db.session.commit()

            # Fetch the player again to check
            check_player = Player.query.get(player.id)
            logger.info(f"After update, {check_player.username}'s games_won is {check_player.games_won} and games_played is {check_player.games_played}")

            return True
        except SQLAlchemyError as e:
            db.session.rollback()  # Rollback any changes if an error occurs
            logger.exception(f"An error occurred while updating player '{player.username}'!")
            return False
        finally:
            db.session.close()
